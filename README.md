# 🚦 No-Helmet Detection & Number Plate Recognition System

An AI-powered traffic monitoring system that automatically detects **motorcyclists without helmets**, extracts their **number plates using OCR**, and stores violation records in **Firebase** with a live **Streamlit dashboard**.

---

## 📌 Project Overview

This project uses **Computer Vision + Deep Learning** to automate traffic rule enforcement.

The system:

1. Detects riders using **YOLOv8**.
2. Identifies whether the rider is wearing a helmet.
3. Detects the vehicle’s number plate.
4. Extracts plate text using **PaddleOCR**.
5. Saves violation data to **Firebase Realtime Database**.
6. Displays violations in a **web dashboard (Streamlit)**.

---

## 🧠 Technologies Used

* Python 3.10
* YOLOv8 (Ultralytics)
* OpenCV
* PaddleOCR
* Firebase Realtime Database
* Streamlit (Frontend Dashboard)
* NumPy

---

## ⚙️ System Workflow

```
Video Input → YOLO Detection → No Helmet Found →
Number Plate Crop → OCR Extraction →
Save Image Locally → Push Data to Firebase →
Display on Streamlit Dashboard
```

---

## 📁 Project Structure

```
no-helmet-numberplate/
│
├── test1.py              # Backend detection script
├── app.py                # Streamlit frontend
├── best.pt               # YOLO trained model
├── vid1.mp4              # Input video
├── requirements.txt      # Dependencies
├── .gitignore
└── README.md
```

---

## 🔐 Firebase Setup (Important)

⚠️ The Firebase service key is NOT included for security.

You must download your own key:

1. Go to **Firebase Console**
2. Project Settings → Service Accounts
3. Click **Generate New Private Key**
4. Download JSON file
5. Place it inside the project folder
6. Update this line in `test1.py` and `app.py`:

```python
cred = credentials.Certificate("your-firebase-key.json")
```

---

## 📦 Installation Steps

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/no-helmet-numberplate.git
cd no-helmet-numberplate
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Windows**

```bash
.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If no requirements file:

```bash
pip install ultralytics opencv-python paddleocr firebase-admin streamlit cvzone numpy
```

---

## ▶️ Running the Project

You must run **backend and frontend in separate terminals**.

---

### 🖥 Terminal 1 — Start Detection Backend

```bash
python test1.py
```

This will:

* Run YOLO detection
* Perform OCR
* Store violations in Firebase

---

### 🌐 Terminal 2 — Start Dashboard

```bash
streamlit run app.py
```

Open browser:

```
http://localhost:8501
```

---

## 📊 Dashboard Features

* Live violation records
* Number plate display
* Date & time of violation
* Saved violation images
* Auto-refreshing data from Firebase

---

## 🧾 Example Firebase Record

```
violations/
   ├── number_plate: MH12AB1234
   ├── date: 2026-02-18
   ├── time: 14:22:31
   └── local_path: /images/MH12AB1234.jpg
```

---

## 📷 Output

Each violation:

* Cropped plate image saved in date folder
* Data logged to Firebase
* Visible instantly on dashboard

---

## ⚠️ Important Notes

* Do NOT upload Firebase JSON key to GitHub.
* Ensure `best.pt` model file is present.
* Use Python **3.10 or 3.11** (recommended).
* Keep backend running while using dashboard.

---

## 🚀 Future Enhancements

* Live CCTV camera integration
* Automatic challan generation
* Email/SMS alerts
* Vehicle owner database linkage
* Cloud deployment (AWS/GCP)

---

## 👩‍💻 Author

**Sneha Yadav**

AI-Based Traffic Monitoring System


---

## 📜 License

This project is for **educational and research purposes only**.
