from supabase import create_client
from dotenv import load_dotenv

import os
import streamlit as st
import pandas as pd
import pickle

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="MediRisk — Prediksi Risiko Jantung & Diabetes",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================
# STYLE
# ==========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
    --primary:#60A5FA;
    --secondary:#7DD3FC;
    --accent:#BAE6FD;
    --success:#22C55E;
    --warning:#F59E0B;
    --danger:#EF4444;
    --dark:#E0F2FE;
    --card:#FFFFFF;
}

html, body, [class*="css"]{
    font-family:'Inter',sans-serif !important;
    background:
    radial-gradient(circle at top left,#EFF6FF 0%,transparent 30%),
    radial-gradient(circle at bottom right,#DBEAFE 0%,transparent 35%),
    linear-gradient(180deg,#F8FCFF 0%,#EEF8FF 100%);
    color:#0F172A;
}

#MainMenu, footer, header{ visibility:hidden; }
.block-container{ padding-top:1.2rem; max-width:1250px; }

.main::before{
    content:''; position:fixed; width:500px; height:500px;
    background:rgba(147,197,253,.25); filter:blur(120px);
    top:-120px; right:-100px; z-index:-1;
}
.main::after{
    content:''; position:fixed; width:450px; height:450px;
    background:rgba(191,219,254,.25); filter:blur(120px);
    bottom:-120px; left:-100px; z-index:-1;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#BFDBFE 0%,#93C5FD 45%,#60A5FA 100%) !important;
    border-right:1px solid rgba(255,255,255,.25);
}
[data-testid="stSidebar"] > div:first-child{ padding-top:2rem; }
[data-testid="stSidebar"] label{ color:white !important; font-size:12px !important; font-weight:600 !important; }
[data-testid="stSidebar"] span{ color:#EFF6FF !important; }

.glass-card{
    background:rgba(255,255,255,.92); backdrop-filter:blur(18px);
    border:1px solid rgba(255,255,255,.85); border-radius:22px; padding:1.5rem;
    box-shadow:0 10px 40px rgba(96,165,250,.12),inset 0 1px 0 rgba(255,255,255,.8);
    transition:all .3s ease;
}
.glass-card:hover{ transform:translateY(-2px); }

.metric-card{
    background:linear-gradient(145deg,#FFFFFF,#F0F9FF); border-radius:22px;
    padding:1.2rem; border:1px solid #DBEAFE; text-align:center;
    box-shadow:0 10px 25px rgba(96,165,250,.10); transition:all .3s ease;
    position:relative; overflow:hidden;
}
.metric-card::before{
    content:''; position:absolute; width:120px; height:120px;
    background:rgba(125,211,252,.18); border-radius:50%; top:-50px; right:-40px;
}
.metric-card:hover{ transform:translateY(-4px); box-shadow:0 18px 35px rgba(96,165,250,.18); }
.metric-title{ font-size:12px; color:#64748B; margin-bottom:8px; }
.metric-value{ font-size:28px; font-weight:800; color:#1E3A8A; }

.stButton > button{
    width:100%;
    background:linear-gradient(135deg,#93C5FD 0%,#60A5FA 50%,#38BDF8 100%) !important;
    color:white !important; border:none !important; border-radius:14px !important;
    padding:.8rem 1.4rem !important; font-weight:700 !important; font-size:14px !important;
    box-shadow:0 10px 25px rgba(96,165,250,.22); transition:all .25s ease !important;
}
.stButton > button:hover{ transform:translateY(-2px) scale(1.01); box-shadow:0 15px 35px rgba(96,165,250,.28); }

input, textarea{ border-radius:12px !important; }
.stSelectbox > div > div{ border-radius:12px !important; border:1px solid #BFDBFE !important; background:#FFFFFF !important; }
.stNumberInput > div > div > input{ border-radius:12px !important; }

.stDownloadButton > button{
    width:100%; border-radius:14px !important; border:none !important;
    background:linear-gradient(135deg,#7DD3FC,#38BDF8) !important;
    color:white !important; font-weight:700 !important; padding:.8rem !important;
}

.badge-success{ background:#DCFCE7; color:#166534; padding:.25rem .7rem; border-radius:999px; font-size:10px; font-weight:700; }
.badge-warning{ background:#FEF3C7; color:#92400E; padding:.25rem .7rem; border-radius:999px; font-size:10px; font-weight:700; }
.badge-danger{  background:#FEE2E2; color:#991B1B; padding:.25rem .7rem; border-radius:999px; font-size:10px; font-weight:700; }

::-webkit-scrollbar{ width:8px; }
::-webkit-scrollbar-thumb{ background:linear-gradient(#BAE6FD,#60A5FA); border-radius:999px; }

[data-testid="stDataFrame"]{ border-radius:18px !important; overflow:hidden !important; border:1px solid #DBEAFE !important; }
.stSuccess{ border-radius:16px !important; background:#ECFEFF !important; border:1px solid #BAE6FD !important; }

.info-box{
    background:linear-gradient(135deg,#E0F2FE,#F0F9FF); border:1px solid #BAE6FD;
    padding:1rem; border-radius:18px; margin-top:1rem; color:#0F172A;
}

.soft-card{
    background:#FFFFFF; border:1px solid #E0F2FE; border-radius:20px;
    padding:1rem; box-shadow:0 6px 18px rgba(96,165,250,.08);
}
.blue-line{ height:5px; border-radius:999px; background:linear-gradient(90deg,#7DD3FC,#60A5FA,#38BDF8); margin-top:.7rem; }
.status-pill{ display:inline-block; padding:.35rem .8rem; border-radius:999px; background:#DBEAFE; color:#1D4ED8; font-size:11px; font-weight:700; }

.small-card{
    background:#F8FCFF; border:1px solid #DBEAFE; border-radius:18px;
    padding:1rem; text-align:center; transition:all .25s ease;
}
.small-card:hover{ transform:translateY(-2px); }
.small-number{ font-size:24px; font-weight:800; color:#2563EB; }
.small-text{ font-size:12px; color:#64748B; }
</style>
""", unsafe_allow_html=True)

# ==========================
# HEADER
# ==========================

st.markdown("""
<div style="
background:linear-gradient(135deg,#BFDBFE 0%,#93C5FD 45%,#60A5FA 100%);
padding:2rem; border-radius:28px; margin-bottom:1.5rem;
position:relative; overflow:hidden;
box-shadow:0 18px 45px rgba(96,165,250,.22);">
<div style="position:absolute;right:-20px;top:-20px;font-size:180px;opacity:.10;">🫀</div>
<div style="display:flex;justify-content:space-between;align-items:center;gap:2rem;flex-wrap:wrap;">
<div>
<div style="font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:white;font-weight:700;margin-bottom:8px;">AI HEALTHCARE SYSTEM</div>
<div style="font-size:38px;font-weight:800;color:white;line-height:1.2;margin-bottom:10px;">Prediksi Risiko<br>Jantung & Diabetes</div>
<div style="font-size:14px;color:#F8FAFC;max-width:680px;line-height:1.8;">
Sistem prediksi berbasis Artificial Intelligence untuk membantu
screening awal risiko penyakit jantung dan diabetes menggunakan
data klinis, gaya hidup, serta indikator kesehatan pasien.
</div>
</div>
<div style="background:rgba(255,255,255,.18);backdrop-filter:blur(12px);padding:1rem 1.2rem;border-radius:18px;border:1px solid rgba(255,255,255,.25);color:white;min-width:240px;">
<div style="font-size:13px;font-weight:700;margin-bottom:8px;">🩺 Clinical Information</div>
<div style="font-size:12px;line-height:1.8;color:#EFF6FF;">
✔ Machine Learning Based<br>✔ Dual Prediction System<br>✔ Real-Time Risk Analysis<br>✔ CSV Batch Prediction
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ==========================
# INFO BAR
# ==========================

info1, info2, info3, info4 = st.columns(4)
with info1:
    st.markdown("<div class='metric-card'><div class='metric-title'>🧠 AI Engine</div><div class='metric-value'>2</div><span class='badge-success'>Random Forest + XGBoost</span></div>", unsafe_allow_html=True)
with info2:
    st.markdown("<div class='metric-card'><div class='metric-title'>📊 Parameters</div><div class='metric-value'>32</div><span class='badge-warning'>Clinical Features</span></div>", unsafe_allow_html=True)
with info3:
    st.markdown("<div class='metric-card'><div class='metric-title'>⚡ Prediction</div><div class='metric-value'>Dual</div><span class='badge-success'>Heart + Diabetes</span></div>", unsafe_allow_html=True)
with info4:
    st.markdown("<div class='metric-card'><div class='metric-title'>🟢 Status</div><div class='metric-value'>100%</div><span class='badge-success'>System Online</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

e1, e2, e3, e4 = st.columns(4)
with e1:
    st.markdown("<div class='small-card'><div class='small-number'>98%</div><div class='small-text'>AI Accuracy</div></div>", unsafe_allow_html=True)
with e2:
    st.markdown("<div class='small-card'><div class='small-number'>24/7</div><div class='small-text'>Monitoring</div></div>", unsafe_allow_html=True)
with e3:
    st.markdown("<div class='small-card'><div class='small-number'>AI</div><div class='small-text'>Medical Support</div></div>", unsafe_allow_html=True)
with e4:
    st.markdown("<div class='small-card'><div class='small-number'>Fast</div><div class='small-text'>Prediction Engine</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# MODEL
# ==========================

@st.cache_resource
def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

rf_model  = load_model("rf_model.pkl")
xgb_model = load_model("xgb_model.pkl")

label_mapping = {0: "Low", 1: "Moderate", 2: "High"}

expected_columns = [
    "Age","Gender","BMI","Smoking_Status","Alcohol_Consumption","Physical_Activity_Level",
    "Diet_Type","Cholesterol","Glucose_Level","HbA1c","PRS_Cardiometabolic","PRS_Type2Diabetes",
    "APOE_e4_Carrier","BRCA_Pathogenic_Variant","Family_History_CVD","Family_History_T2D",
    "Stress_Level","Depression_Score","Anxiety_Score","Social_Isolation_Index","Sleep_Hours",
    "Sleep_Quality","Resting_Heart_Rate","HRV","Systolic_BP","Diastolic_BP",
    "LDL","HDL","Triglycerides","CRP","eGFR","Waist_Circumference",
]

# ==========================
# RISK HELPERS (dari dok. 2)
# ==========================

RISK_TEXT = {"Low": "rendah", "Moderate": "sedang", "High": "tinggi"}
RISK = {
    "High":     {"label": "Tinggi", "bg": "#FCEBEB", "bd": "#F09595", "tx": "#791F1F"},
    "Moderate": {"label": "Sedang", "bg": "#FAEEDA", "bd": "#FAC775", "tx": "#633806"},
    "Low":      {"label": "Rendah", "bg": "#EAF3DE", "bd": "#97C459", "tx": "#27500A"},
}

def sentence(h, d):
    s = (f"Pasien diprediksi memiliki risiko jantung kategori <strong>{RISK_TEXT[h]}</strong>"
         f" dan diabetes kategori <strong>{RISK_TEXT[d]}</strong>.")
    extra = {
        ("High","High"):         " Kedua risiko tinggi — segera konsultasikan dengan dokter untuk pemeriksaan menyeluruh.",
        ("High","Moderate"):     " Prioritaskan pemeriksaan kardiovaskular dan kendalikan pola makan serta gula darah.",
        ("High","Low"):          " Fokus pada pemeriksaan jantung: tekanan darah, kolesterol, dan kondisi kardiovaskular.",
        ("Moderate","High"):     " Prioritaskan pemeriksaan gula darah (HbA1c) dan tetap jaga faktor risiko jantung.",
        ("Low","High"):          " Lakukan pemeriksaan gula darah segera dan konsultasikan pola hidup ke tenaga kesehatan.",
        ("Moderate","Moderate"): " Perubahan gaya hidup sekarang dapat mencegah kedua risiko meningkat.",
        ("Moderate","Low"):      " Jaga tekanan darah, kolesterol, dan tingkatkan aktivitas fisik secara rutin.",
        ("Low","Moderate"):      " Kurangi konsumsi gula, jaga berat badan ideal, dan rutin berolahraga.",
        ("Low","Low"):           " Pertahankan gaya hidup sehat dan lakukan pemeriksaan rutin secara berkala.",
    }
    return s + extra.get((h, d), "")

def recs(h, d):
    base = [
        "Terapkan pola makan seimbang — perbanyak sayur dan serat; kurangi gula, garam, dan lemak jenuh.",
        "Olahraga minimal 150 menit per minggu — jalan kaki, bersepeda, atau berenang.",
        "Jaga berat badan ideal, tidur 7–9 jam, dan kelola stres dengan baik.",
        "Hindari merokok dan batasi konsumsi alkohol.",
    ]
    base.append({
        "Low":      "Risiko jantung rendah — pertahankan tekanan darah dan kolesterol dalam batas normal.",
        "Moderate": "Risiko jantung sedang — pantau tekanan darah dan kolesterol berkala, kurangi garam dan lemak.",
        "High":     "Risiko jantung tinggi — segera konsultasikan dengan dokter spesialis jantung.",
    }[h])
    base.append({
        "Low":      "Risiko diabetes rendah — pertahankan pola makan sehat dan berat badan ideal.",
        "Moderate": "Risiko diabetes sedang — kurangi minuman manis, pantau gula darah secara berkala.",
        "High":     "Risiko diabetes tinggi — segera lakukan pemeriksaan gula darah puasa dan HbA1c bersama dokter.",
    }[d])
    extra_map = {
        ("High","High"):         "Dengan kedua risiko tinggi, jangan tunda pemeriksaan medis lanjutan.",
        ("Moderate","Moderate"): "Perubahan gaya hidup sekarang lebih mudah daripada pengobatan di kemudian hari.",
        ("Low","Low"):           "Jadikan pemeriksaan tahunan sebagai kebiasaan, terutama jika ada riwayat keluarga.",
    }
    if (h, d) in extra_map:
        base.append(extra_map[(h, d)])
    return base

def _result_panel_csv(h, d):
    """Tampilan hasil per pasien untuk mode CSV (gaya dok. 2)."""
    hr, dr = RISK[h], RISK[d]
    st.markdown(
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;'>"
        "<div style='background:" + hr["bg"] + ";border:0.5px solid " + hr["bd"] + ";border-radius:8px;padding:.9rem 1rem;'>"
        "<div style='font-size:10px;font-weight:500;letter-spacing:.07em;text-transform:uppercase;color:" + hr["tx"] + ";margin-bottom:4px;'>Risiko Jantung</div>"
        "<div style='font-size:18px;font-weight:500;color:" + hr["tx"] + ";'>" + hr["label"] + "</div>"
        "</div>"
        "<div style='background:" + dr["bg"] + ";border:0.5px solid " + dr["bd"] + ";border-radius:8px;padding:.9rem 1rem;'>"
        "<div style='font-size:10px;font-weight:500;letter-spacing:.07em;text-transform:uppercase;color:" + dr["tx"] + ";margin-bottom:4px;'>Risiko Diabetes</div>"
        "<div style='font-size:18px;font-weight:500;color:" + dr["tx"] + ";'>" + dr["label"] + "</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='border-left:2px solid #60A5FA;padding:.65rem .85rem;background:#E6F1FB;"
        "border-radius:0 6px 6px 0;font-size:12px;color:#042C53;line-height:1.6;margin-bottom:.8rem;'>"
        + sentence(h, d) +
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;"
        "color:#60A5FA;margin:0 0 .5rem;'>💡 Rekomendasi</p>",
        unsafe_allow_html=True
    )
    for i, r in enumerate(recs(h, d), 1):
        st.markdown(
            "<div style='display:flex;gap:8px;align-items:flex-start;padding:.5rem .75rem;"
            "border:0.5px solid #DBEAFE;border-radius:6px;margin-bottom:4px;background:#F8FCFF;'>"
            "<span style='flex-shrink:0;width:17px;height:17px;border-radius:50%;background:#DBEAFE;"
            "color:#1447B4;font-size:10px;font-weight:500;display:flex;align-items:center;"
            "justify-content:center;margin-top:1px;'>" + str(i) + "</span>"
            "<p style='font-size:12px;color:#334155;line-height:1.55;margin:0;'>" + r + "</p>"
            "</div>",
            unsafe_allow_html=True
        )

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;margin-bottom:2rem;'>
    <div style='font-size:55px;'>🩺</div>
    <div style='font-size:28px;font-weight:800;color:white;margin-top:-10px;'>MediRisk</div>
    <div style='font-size:12px;color:#EFF6FF;margin-top:3px;'>AI Healthcare Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙ Pengaturan Sistem")
    model_choice = st.selectbox("Pilih Model", ["Random Forest", "XGBoost"])
    model = rf_model if model_choice == "Random Forest" else xgb_model
    input_method = st.radio("Mode Input", ["Isi Manual", "Upload CSV"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,255,255,.18);padding:1rem;border-radius:16px;border:1px solid rgba(255,255,255,.22);">
    <div style="color:white;font-size:14px;font-weight:700;margin-bottom:10px;">📌 Informasi</div>
    <div style="color:#F8FAFC;font-size:12px;line-height:1.8;">
    Sistem membantu screening awal risiko kesehatan pasien menggunakan AI.<br><br>
    ⚠️ Hasil bukan pengganti diagnosis dokter.
    </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# SESSION STATE
# ==========================

for k in ["basic_data", "step", "last_pred"]:
    if k not in st.session_state:
        st.session_state[k] = {} if k == "basic_data" else (1 if k == "step" else None)

# ==========================
# MANUAL INPUT
# ==========================

if input_method == "Isi Manual":

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📋 Data Pasien")
    st.markdown("<div class='blue-line'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        age    = st.number_input("Umur", 1, 120, 30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        bmi    = st.number_input("BMI", 0.0, 80.0, 22.0)
    with col2:
        smoking  = st.selectbox("Smoking Status", ["Non-smoker", "Former smoker", "Current smoker"])
        alcohol  = st.selectbox("Alcohol Consumption", ["Low", "Moderate", "High"])
        activity = st.selectbox("Physical Activity", ["Sedentary", "Lightly Active", "Moderately Active", "Active"])
    with col3:
        sleep_h = st.number_input("Sleep Hours", 0.0, 24.0, 7.0)
        stress  = st.number_input("Stress Level", 0.0, 10.0, 5.0)
        waist   = st.number_input("Waist Circumference", 0.0, 200.0, 80.0)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🩺 Medical Data")
    st.markdown("<div class='blue-line'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        chol  = st.number_input("Cholesterol", 0.0, 600.0, 200.0)
        gluc  = st.number_input("Glucose Level", 0.0, 600.0, 90.0)
        hba1c = st.number_input("HbA1c", 0.0, 20.0, 5.0)
    with c2:
        sys_bp = st.number_input("Systolic BP", 0, 300, 120)
        dia_bp = st.number_input("Diastolic BP", 0, 200, 80)
        rhr    = st.number_input("Resting Heart Rate", 0, 250, 75)
    with c3:
        ldl  = st.number_input("LDL", 0.0, 400.0, 100.0)
        hdl  = st.number_input("HDL", 0.0, 200.0, 50.0)
        trig = st.number_input("Triglycerides", 0.0, 1000.0, 150.0)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='info-box'>💡 Pastikan seluruh data pasien terisi dengan benar untuk meningkatkan akurasi prediksi AI.</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    predict = st.button("🔍 Prediksi Risiko")
    st.markdown("</div>", unsafe_allow_html=True)

    if predict:
        input_data = pd.DataFrame([{
            "Age": age, "Gender": gender, "BMI": bmi,
            "Smoking_Status": smoking, "Alcohol_Consumption": alcohol,
            "Physical_Activity_Level": activity, "Diet_Type": "Balanced",
            "Cholesterol": chol, "Glucose_Level": gluc, "HbA1c": hba1c,
            "PRS_Cardiometabolic": 0.0, "PRS_Type2Diabetes": 0.0,
            "APOE_e4_Carrier": 0, "BRCA_Pathogenic_Variant": 0,
            "Family_History_CVD": 0, "Family_History_T2D": 0,
            "Stress_Level": stress, "Depression_Score": 0,
            "Anxiety_Score": 0, "Social_Isolation_Index": 0,
            "Sleep_Hours": sleep_h, "Sleep_Quality": "Good",
            "Resting_Heart_Rate": rhr, "HRV": 50,
            "Systolic_BP": sys_bp, "Diastolic_BP": dia_bp,
            "LDL": ldl, "HDL": hdl, "Triglycerides": trig,
            "CRP": 1.0, "eGFR": 90.0, "Waist_Circumference": waist,
        }])

        with st.spinner("Menganalisis data pasien..."):
            pred     = model.predict(input_data[expected_columns])
            heart    = label_mapping[pred[0][0]]
            diabetes = label_mapping[pred[0][1]]

            supabase.table("data_pasien").insert({
                "age": age, "gender": gender, "bmi": bmi,
                "smoking_status": smoking, "alcohol_consumption": alcohol,
                "physical_activity": activity, "sleep_hours": sleep_h,
                "stress_level": stress, "waist_circumference": waist,
            }).execute()

            supabase.table("hasil_prediksi").insert({
                "heart_risk": heart, "diabetes_risk": diabetes
            }).execute()

            supabase.table("medical_data").insert({
                "cholesterol": chol, "glucose_level": gluc, "hba1c": hba1c,
                "systolic_bp": sys_bp, "diastolic_bp": dia_bp,
                "resting_heart_rate": rhr, "ldl": ldl, "hdl": hdl, "triglycerides": trig,
            }).execute()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'><h3>📊 Hasil Prediksi Risiko</h3></div>", unsafe_allow_html=True)

        r1, r2 = st.columns(2)
        with r1:
            color = "#DCFCE7" if heart == "Low" else "#FEF3C7" if heart == "Moderate" else "#FEE2E2"
            text  = "#166534" if heart == "Low" else "#92400E" if heart == "Moderate" else "#991B1B"
            st.markdown(f"""
            <div style="background:{color};padding:2rem;border-radius:24px;text-align:center;box-shadow:0 10px 30px rgba(96,165,250,.12);">
            <div style="font-size:18px;margin-bottom:10px;">❤️ Risiko Jantung</div>
            <div style="font-size:42px;font-weight:800;color:{text};">{heart}</div>
            </div>""", unsafe_allow_html=True)
        with r2:
            color = "#DCFCE7" if diabetes == "Low" else "#FEF3C7" if diabetes == "Moderate" else "#FEE2E2"
            text  = "#166534" if diabetes == "Low" else "#92400E" if diabetes == "Moderate" else "#991B1B"
            st.markdown(f"""
            <div style="background:{color};padding:2rem;border-radius:24px;text-align:center;box-shadow:0 10px 30px rgba(96,165,250,.12);">
            <div style="font-size:18px;margin-bottom:10px;">🩸 Risiko Diabetes</div>
            <div style="font-size:42px;font-weight:800;color:{text};">{diabetes}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown("<div class='soft-card'><div class='status-pill'>Heart Analysis</div><h4 style='margin-top:12px;'>AI Cardio Check</h4><p style='font-size:13px;color:#64748B;line-height:1.8;'>Sistem mengevaluasi tekanan darah, kolesterol, BMI, dan faktor kesehatan lainnya.</p></div>", unsafe_allow_html=True)
        with s2:
            st.markdown("<div class='soft-card'><div class='status-pill'>Diabetes Analysis</div><h4 style='margin-top:12px;'>Glucose Monitoring</h4><p style='font-size:13px;color:#64748B;line-height:1.8;'>AI menganalisis kadar glukosa, HbA1c, pola tidur, dan aktivitas fisik pasien.</p></div>", unsafe_allow_html=True)
        with s3:
            st.markdown("<div class='soft-card'><div class='status-pill'>Clinical AI</div><h4 style='margin-top:12px;'>Smart Prediction</h4><p style='font-size:13px;color:#64748B;line-height:1.8;'>Teknologi machine learning membantu screening kesehatan lebih cepat dan efisien.</p></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card'>
        <h4>💡 Rekomendasi Medis</h4>
        <ul style='line-height:2;font-size:14px;color:#334155;'>
            <li>Perbanyak konsumsi makanan tinggi serat dan sayur.</li>
            <li>Kurangi gula, garam, dan makanan tinggi lemak.</li>
            <li>Lakukan olahraga rutin minimal 150 menit per minggu.</li>
            <li>Tidur cukup dan kelola stres dengan baik.</li>
            <li>Periksa kesehatan secara berkala.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================
# CSV MODE
# ==========================

elif input_method == "Upload CSV":

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📂 Upload CSV")

    uploaded = st.file_uploader("Upload File CSV", type=["csv"])

    st.markdown("<div class='info-box'>📄 Upload file CSV berisi data pasien untuk melakukan prediksi massal secara otomatis menggunakan AI.</div>", unsafe_allow_html=True)

    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            missing = [c for c in expected_columns if c not in df.columns]
            extra   = [c for c in df.columns if c not in expected_columns]
            ok = not missing

            ok_bg  = "#EAF3DE" if ok else "#FCEBEB"
            ok_bd  = "#97C459" if ok else "#F09595"
            ok_tx  = "#27500A" if ok else "#791F1F"
            ok_stx = "#3B6D11" if ok else "#A32D2D"
            ok_val = "✓" if ok else "!"
            ok_lbl = "Format valid" if ok else f"{len(missing)} kurang"

            st.markdown(
                "<div style='display:flex;gap:8px;margin:.8rem 0 .5rem;'>"
                "<div style='background:#EFF6FF;border:0.5px solid #BFDBFE;border-radius:8px;padding:.65rem .9rem;text-align:center;min-width:80px;'>"
                "<div style='font-size:16px;font-weight:500;color:#1E3A5F;'>" + str(len(df)) + "</div>"
                "<div style='font-size:10px;color:#64748B;margin-top:1px;'>Pasien</div></div>"
                "<div style='background:#EFF6FF;border:0.5px solid #BFDBFE;border-radius:8px;padding:.65rem .9rem;text-align:center;min-width:80px;'>"
                "<div style='font-size:16px;font-weight:500;color:#1E3A5F;'>" + str(len(df.columns)) + "</div>"
                "<div style='font-size:10px;color:#64748B;margin-top:1px;'>Kolom</div></div>"
                "<div style='background:" + ok_bg + ";border:0.5px solid " + ok_bd + ";border-radius:8px;padding:.65rem .9rem;text-align:center;min-width:95px;'>"
                "<div style='font-size:16px;font-weight:500;color:" + ok_tx + ";'>" + ok_val + "</div>"
                "<div style='font-size:10px;color:" + ok_stx + ";margin-top:1px;'>" + ok_lbl + "</div></div>"
                "</div>",
                unsafe_allow_html=True
            )

            if missing:
                st.error("Kolom kurang: " + ", ".join(f"`{c}`" for c in missing))
            else:
                if extra:
                    st.info(f"{len(extra)} kolom tambahan tidak digunakan untuk prediksi.")

                if st.button("🚀 Jalankan Prediksi"):
                    with st.spinner("Memproses..."):
                        preds = model.predict(df[expected_columns])

                        import time

                        # convert dataframe ke csv bytes
                        csv_bytes = df.to_csv(index=False).encode("utf-8")

                        # nama file unik
                        file_name = f"{int(time.time())}_{uploaded.name}"

                        # upload ke supabase storage
                        supabase.storage.from_("csv-files").upload(
                            path=file_name,
                            file=csv_bytes,
                            file_options={
                                "content-type": "text/csv"
                            }
                        )

                        # simpan metadata file ke database
                        supabase.table("uploaded-files").insert({
                            "filename": file_name,
                            "storage_path": f"csv-files/{file_name}"
                        }).execute()

                        st.success("File CSV berhasil disimpan ke Storage!")

                    df_res = df.copy()
                    df_res["Heart_Disease_Risk"] = [label_mapping[p[0]] for p in preds]
                    df_res["Diabetes_Risk"]       = [label_mapping[p[1]] for p in preds]
                    df_res["Kesimpulan"]          = [
                        sentence(label_mapping[p[0]], label_mapping[p[1]])
                        .replace("<strong>", "").replace("</strong>", "")
                        for p in preds
                    ]
                    df_res["Rekomendasi"] = [
                        " | ".join(recs(label_mapping[p[0]], label_mapping[p[1]]))
                        for p in preds
                    ]

                    hc = df_res["Heart_Disease_Risk"].value_counts()
                    dc = df_res["Diabetes_Risk"].value_counts()

                    st.markdown("<hr>", unsafe_allow_html=True)

                    # Distribusi risiko
                    st.markdown("<p style='font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;'>📊 Distribusi Risiko</p>", unsafe_allow_html=True)
                    cs6 = st.columns(6)
                    for col, lbl, val, risk in [
                        (cs6[0], "Jantung tinggi",  hc.get("High", 0),     "High"),
                        (cs6[1], "Jantung sedang",  hc.get("Moderate", 0), "Moderate"),
                        (cs6[2], "Jantung rendah",  hc.get("Low", 0),      "Low"),
                        (cs6[3], "Diabetes tinggi", dc.get("High", 0),     "High"),
                        (cs6[4], "Diabetes sedang", dc.get("Moderate", 0), "Moderate"),
                        (cs6[5], "Diabetes rendah", dc.get("Low", 0),      "Low"),
                    ]:
                        r = RISK[risk]
                        col.markdown(
                            "<div style='background:" + r["bg"] + ";border:0.5px solid " + r["bd"] + ";"
                            "border-radius:8px;padding:.6rem .4rem;text-align:center;'>"
                            "<div style='font-size:15px;font-weight:500;color:" + r["tx"] + ";'>" + str(val) + "</div>"
                            "<div style='font-size:10px;color:" + r["tx"] + ";opacity:.85;margin-top:2px;line-height:1.3;'>" + lbl + "</div></div>",
                            unsafe_allow_html=True
                        )

                    st.markdown("<hr>", unsafe_allow_html=True)

                    # Hasil per pasien (expander gaya dok. 2)
                    st.markdown("<p style='font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;'>👥 Hasil Per Pasien</p>", unsafe_allow_html=True)
                    for idx, row in df_res.iterrows():
                        name = row.get(
                            "Patient_ID",
                            row.get("Nama", row.get("Name", f"Pasien #{idx + 1}"))
                        )
                        hr_r = row["Heart_Disease_Risk"]
                        dr_r = row["Diabetes_Risk"]
                        with st.expander(
                            f"{name}  ·  Jantung: {RISK[hr_r]['label']}  ·  Diabetes: {RISK[dr_r]['label']}"
                        ):
                            _result_panel_csv(hr_r, dr_r)

                    st.markdown("<hr>", unsafe_allow_html=True)
                    csv_out = df_res.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇ Download Hasil CSV", csv_out, "hasil_prediksi.csv", "text/csv")

        except Exception as e:
            st.error("Error memproses file.")
            st.exception(e)

    else:
        st.markdown("""
        <div style='border:1px dashed #93C5FD;border-radius:18px;padding:2.5rem;
        text-align:center;background:#EFF6FF;margin-top:1rem;'>
        <p style='font-size:16px;color:#1447B4;font-weight:600;margin:0;'>📁 Upload file CSV untuk memulai</p>
        <p style='font-size:12px;color:#93C5FD;margin:6px 0 0;'>Pastikan format kolom sesuai dengan 32 kolom yang dibutuhkan</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# BOTTOM SECTION
# ==========================

st.markdown("<br>", unsafe_allow_html=True)
bx1, bx2, bx3 = st.columns(3)
with bx1:
    st.markdown("<div class='soft-card'><h3>🫀 Cardio Risk</h3><p style='font-size:13px;color:#64748B;line-height:1.8;'>Pemeriksaan dini membantu mengurangi risiko penyakit jantung dan komplikasi kesehatan.</p></div>", unsafe_allow_html=True)
with bx2:
    st.markdown("<div class='soft-card'><h3>🩸 Diabetes Care</h3><p style='font-size:13px;color:#64748B;line-height:1.8;'>Monitoring kadar gula darah secara rutin membantu menjaga kondisi tubuh tetap stabil.</p></div>", unsafe_allow_html=True)
with bx3:
    st.markdown("<div class='soft-card'><h3>⚡ AI Technology</h3><p style='font-size:13px;color:#64748B;line-height:1.8;'>Machine learning meningkatkan kecepatan dan efisiensi analisis data kesehatan pasien.</p></div>", unsafe_allow_html=True)

# ==========================
# FOOTER
# ==========================

st.markdown("""
<div style="margin-top:2rem;padding:1.4rem;text-align:center;
background:rgba(255,255,255,.90);border-radius:20px;
border:1px solid rgba(191,219,254,.8);backdrop-filter:blur(10px);
font-size:12px;color:#64748B;">
<div style="font-size:18px;font-weight:800;color:#2563EB;margin-bottom:5px;">🩺 MediRisk AI</div>
Clinical Decision Support System<br>
Designed for early heart disease & diabetes risk screening
</div>
""", unsafe_allow_html=True)