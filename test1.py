import os
import cv2
import numpy as np
from ultralytics import YOLO
import cvzone
from paddleocr import PaddleOCR
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

# ------------------- Firebase Setup -------------------
cred = credentials.Certificate("numberplate-5735e-firebase-adminsdk-fbsvc-9c9eb37d24.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://numberplate-5735e-default-rtdb.firebaseio.com/"
})

violations_ref = db.reference("violations")


# ------------------- Initialize PaddleOCR -------------------
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)

# ------------------- OCR Function -------------------
def perform_ocr(image_array):
    """Run OCR on cropped plate image and return text."""
    if image_array is None or image_array.size == 0:
        return ""
    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    results = ocr.ocr(image_array)
    plate_text = ""
    if results and isinstance(results, list) and "rec_texts" in results[0]:
        plate_text = " ".join(results[0]["rec_texts"]).strip()
    elif results and results[0]:
        detected_text = [res[1][0] for res in results[0] if len(res) > 1]
        plate_text = "".join(detected_text).strip()
    return plate_text

# ------------------- Create Date Folder -------------------
def get_date_folder():
    """Create folder named with current date (YYYY-MM-DD) if not exists."""
    folder_name = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# ------------------- Load YOLO -------------------
model = YOLO("best.pt")  # Replace with your YOLO weights
names = model.names
area = [(1, 173), (62, 468), (608, 431), (364, 155)]
processed_track_ids = set()

cap = cv2.VideoCapture('vid1.mp4')  # Replace with your video file

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1020, 500))
    results = model.track(frame, persist=True)

    no_helmet_detected = False
    numberplate_box = None
    numberplate_track_id = None

    if results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.int().cpu().tolist()
        class_ids = results[0].boxes.cls.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        for box, class_id, track_id in zip(boxes, class_ids, track_ids):
            c = names[class_id]
            x1, y1, x2, y2 = box
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Check if inside polygon
            result = cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False)
            if result >= 0:
                if c == 'no-helmet':
                    no_helmet_detected = True
                elif c == 'numberplate':
                    numberplate_box = box
                    numberplate_track_id = track_id

        # Process violation
        if no_helmet_detected and numberplate_box and numberplate_track_id not in processed_track_ids:
            x1, y1, x2, y2 = numberplate_box
            pad = 10
            x1, y1 = max(0, x1 - pad), max(0, y1 - pad)
            x2, y2 = min(frame.shape[1], x2 + pad), min(frame.shape[0], y2 + pad)

            crop = frame[y1:y2, x1:x2]
            crop = cv2.resize(crop, (200, 200))

            # OCR detection
            plate_text = perform_ocr(crop)

            # Save to current date folder
            folder = get_date_folder()
            current_time = datetime.now().strftime('%H-%M-%S-%f')[:12]
            filename = f"{plate_text}_{current_time}.jpg"
            save_path = os.path.join(folder, filename)
            cv2.imwrite(save_path, crop)

            # Push to Firebase Realtime DB
            violations_ref.push({
                "number_plate": plate_text,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "time": datetime.now().strftime('%H:%M:%S'),
                "local_path": os.path.abspath(save_path)
            })

            processed_track_ids.add(numberplate_track_id)

    # Draw polygon and show frame
    cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 255), 2)
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
