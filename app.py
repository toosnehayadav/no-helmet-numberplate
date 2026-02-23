import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import os

# ------------------ Firebase Connection ------------------
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://numberplate-5735e-default-rtdb.firebaseio.com/"
    })

ref = db.reference("violations")

# ------------------ Page Config ------------------
st.set_page_config(page_title="Helmet Violation System", layout="wide")

# ------------------ Custom UI ------------------
st.markdown("""
    <style>
    .main-title {
        font-size:40px;
        font-weight:700;
        color:#FF4B4B;
    }
    .sub-text {
        color:gray;
        font-size:18px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚨 Helmet Violation Detection Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">AI-Based Traffic Monitoring System</p>', unsafe_allow_html=True)

st.divider()

# ------------------ Fetch Data ------------------
data = ref.get()

if not data:
    st.warning("No violations detected yet...")
    st.stop()

violations = []
for key, value in data.items():
    value["id"] = key
    violations.append(value)

df = pd.DataFrame(violations)

# ------------------ Metrics ------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Violations", len(df))

with col2:
    today = pd.Timestamp.now().strftime('%Y-%m-%d')
    today_count = len(df[df["date"] == today]) if "date" in df else 0
    st.metric("Today's Violations", today_count)

st.divider()

# ------------------ Table ------------------
st.subheader("📊 Violation Records")
st.dataframe(df, use_container_width=True)

# ------------------ Download CSV ------------------
st.subheader("⬇ Download Report")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="helmet_violations.csv",
    mime="text/csv",
)

st.divider()

# ------------------ Image Viewer ------------------
st.subheader("📸 Violation Image Preview")

selected_plate = st.selectbox(
    "Select Number Plate",
    df["number_plate"].astype(str)
)

selected_row = df[df["number_plate"].astype(str) == selected_plate].iloc[0]

image_path = selected_row.get("local_path", "")

if image_path and os.path.exists(image_path):
    st.image(image_path, caption=f"Plate: {selected_plate}", width=400)
else:
    st.warning("Image not found locally. Check backend save path.")

st.divider()

# ------------------ Auto Refresh ------------------
st.caption("🔄 Dashboard auto-refreshes when reloaded.")
