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
    --primary:#60A5FA; --secondary:#7DD3FC; --accent:#BAE6FD;
    --success:#22C55E; --warning:#F59E0B; --danger:#EF4444;
    --dark:#E0F2FE; --card:#FFFFFF;
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
    transition:all .3s ease; margin-bottom:1rem;
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

.step-bar{
    display:flex; gap:0; margin-bottom:1.2rem;
    border:1px solid #DBEAFE; border-radius:14px; overflow:hidden;
}
.step-active{
    flex:1; padding:.6rem 1rem; background:#60A5FA;
    color:white; font-size:13px; font-weight:700; text-align:center;
}
.step-done{
    flex:1; padding:.6rem 1rem; background:#DBEAFE;
    color:#1E40AF; font-size:13px; font-weight:600; text-align:center;
}
.step-inactive{
    flex:1; padding:.6rem 1rem; background:#F8FCFF;
    color:#94A3B8; font-size:13px; font-weight:500; text-align:center;
    border-left:1px solid #DBEAFE;
}
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
# RISK HELPERS
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

def show_result_panel(h, d):
    """Tampilan hasil prediksi gaya dokumen 2 — kartu berwarna + kalimat + rekomendasi."""
    hr, dr = RISK[h], RISK[d]

    # Kartu risiko
    st.markdown(
        f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;'>"
        f"<div style='background:{hr['bg']};border:1px solid {hr['bd']};border-radius:14px;padding:1.1rem 1.2rem;'>"
        f"<div style='font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:{hr['tx']};margin-bottom:6px;'>❤️ Risiko Jantung</div>"
        f"<div style='font-size:26px;font-weight:800;color:{hr['tx']};'>{hr['label']}</div>"
        f"<div style='font-size:11px;color:{hr['tx']};opacity:.75;margin-top:3px;'>{h}</div>"
        f"</div>"
        f"<div style='background:{dr['bg']};border:1px solid {dr['bd']};border-radius:14px;padding:1.1rem 1.2rem;'>"
        f"<div style='font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:{dr['tx']};margin-bottom:6px;'>🩸 Risiko Diabetes</div>"
        f"<div style='font-size:26px;font-weight:800;color:{dr['tx']};'>{dr['label']}</div>"
        f"<div style='font-size:11px;color:{dr['tx']};opacity:.75;margin-top:3px;'>{d}</div>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Kalimat kesimpulan
    st.markdown(
        f"<div style='border-left:3px solid #60A5FA;padding:.7rem 1rem;background:#E6F1FB;"
        f"border-radius:0 10px 10px 0;font-size:13px;color:#042C53;line-height:1.7;margin-bottom:1rem;'>"
        f"{sentence(h, d)}</div>",
        unsafe_allow_html=True
    )

    # Rekomendasi
    st.markdown(
        "<p style='font-size:10px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;"
        "color:#60A5FA;margin:0 0 .6rem;'>💡 Rekomendasi Kesehatan</p>",
        unsafe_allow_html=True
    )
    for i, r in enumerate(recs(h, d), 1):
        st.markdown(
            f"<div style='display:flex;gap:10px;align-items:flex-start;padding:.55rem .85rem;"
            f"border:1px solid #DBEAFE;border-radius:10px;margin-bottom:5px;background:#F8FCFF;'>"
            f"<span style='flex-shrink:0;width:20px;height:20px;border-radius:50%;background:#DBEAFE;"
            f"color:#1447B4;font-size:10px;font-weight:700;display:flex;align-items:center;"
            f"justify-content:center;margin-top:1px;'>{i}</span>"
            f"<p style='font-size:12px;color:#334155;line-height:1.6;margin:0;'>{r}</p></div>",
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

    step = st.session_state.step

    # Step bar
    step1_class = "step-active" if step == 1 else "step-done"
    step2_class = "step-active" if step == 2 else ("step-inactive" if step == 1 else "step-done")
    st.markdown(
        f"<div class='step-bar'>"
        f"<div class='{step1_class}'>{'✓ ' if step > 1 else ''}1 · Data Pasien</div>"
        f"<div class='{step2_class}'>2 · Data Medis & Prediksi</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ── STEP 1: DATA PASIEN ─────────────────────────────────────────────
    if step == 1:
        st.subheader("📋 Step 1 — Data Pasien")
        st.markdown("<div class='blue-line'></div><br>", unsafe_allow_html=True)

        with st.form("form_step1"):
            st.markdown("**🧍 Informasi Dasar**")
            col1, col2, col3 = st.columns(3)
            with col1:
                age    = st.number_input("Umur (tahun)", 1, 120, 30)
                gender = st.selectbox("Gender", ["Male", "Female"])
                bmi    = st.number_input("BMI", 0.0, 80.0, 22.0, format="%.1f")
            with col2:
                smoking  = st.selectbox("Smoking Status", ["Non-smoker", "Former smoker", "Current smoker"])
                alcohol  = st.selectbox("Alcohol Consumption", ["Low", "Moderate", "High"])
                activity = st.selectbox("Physical Activity", ["Sedentary", "Lightly Active", "Moderately Active", "Active"])
            with col3:
                diet  = st.selectbox("Diet Type", ["Balanced", "Unhealthy", "Vegetarian", "High-protein"])
                waist = st.number_input("Waist Circumference (cm)", 0.0, 200.0, 80.0, format="%.1f")

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("**😴 Gaya Hidup & Psikososial**")
            c1, c2, c3 = st.columns(3)
            with c1:
                sleep_h = st.number_input("Sleep Hours / hari", 0.0, 24.0, 7.0, format="%.1f")
                sleep_q = st.selectbox("Sleep Quality", ["Poor", "Fair", "Good", "Excellent"])
            with c2:
                stress  = st.number_input("Stress Level (0–10)", 0.0, 10.0, 5.0, format="%.1f")
                depress = st.number_input("Depression Score", 0, value=0)
            with c3:
                anxiety = st.number_input("Anxiety Score", 0, value=0)
                social  = st.number_input("Social Isolation Index", 0, value=0)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("**🧬 Riwayat Keluarga**")
            f1, f2 = st.columns(2)
            with f1:
                fam_cvd = st.selectbox("Riwayat Jantung dalam Keluarga", [0, 1], format_func=lambda x: "Tidak Ada" if x == 0 else "Ada")
            with f2:
                fam_t2d = st.selectbox("Riwayat Diabetes dalam Keluarga", [0, 1], format_func=lambda x: "Tidak Ada" if x == 0 else "Ada")

            st.markdown("<br>", unsafe_allow_html=True)
            submitted1 = st.form_submit_button("Simpan & Lanjut ke Data Medis →")

        if submitted1:
            st.session_state.basic_data = {
                "Age": age, "Gender": gender, "BMI": bmi,
                "Smoking_Status": smoking, "Alcohol_Consumption": alcohol,
                "Physical_Activity_Level": activity, "Diet_Type": diet,
                "Waist_Circumference": waist, "Sleep_Hours": sleep_h,
                "Sleep_Quality": sleep_q, "Stress_Level": stress,
                "Depression_Score": depress, "Anxiety_Score": anxiety,
                "Social_Isolation_Index": social,
                "Family_History_CVD": fam_cvd, "Family_History_T2D": fam_t2d,
            }
            st.session_state.step = 2
            st.session_state.last_pred = None
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Tampilkan ringkasan jika sudah pernah mengisi
        if st.session_state.basic_data:
            bd = st.session_state.basic_data
            with st.expander("📄 Lihat data pasien yang sudah disimpan"):
                g1, g2, g3, g4 = st.columns(4)
                g1.markdown(f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;padding:.6rem .8rem;'><div style='font-size:10px;color:#64748B;'>Umur</div><div style='font-size:14px;font-weight:700;color:#1E293B;'>{bd['Age']} tahun</div></div>", unsafe_allow_html=True)
                g2.markdown(f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;padding:.6rem .8rem;'><div style='font-size:10px;color:#64748B;'>Gender</div><div style='font-size:14px;font-weight:700;color:#1E293B;'>{bd['Gender']}</div></div>", unsafe_allow_html=True)
                g3.markdown(f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;padding:.6rem .8rem;'><div style='font-size:10px;color:#64748B;'>BMI</div><div style='font-size:14px;font-weight:700;color:#1E293B;'>{bd['BMI']}</div></div>", unsafe_allow_html=True)
                g4.markdown(f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;padding:.6rem .8rem;'><div style='font-size:10px;color:#64748B;'>Merokok</div><div style='font-size:14px;font-weight:700;color:#1E293B;'>{bd['Smoking_Status']}</div></div>", unsafe_allow_html=True)

    # ── STEP 2: DATA MEDIS ──────────────────────────────────────────────
    elif step == 2:

        # Cek apakah step 1 sudah diisi
        if not st.session_state.basic_data:
            st.markdown("""
            <div style="background:#FEF3C7;border:1px solid #F59E0B;border-radius:16px;
            padding:1.2rem 1.5rem;margin-bottom:1rem;">
            <div style="font-size:15px;font-weight:700;color:#92400E;margin-bottom:6px;">
            ⚠️ Data Pasien Belum Diisi
            </div>
            <div style="font-size:13px;color:#78350F;line-height:1.7;">
            Anda harus mengisi <strong>Step 1 — Data Pasien</strong> terlebih dahulu sebelum dapat mengisi
            data medis dan menjalankan prediksi. Klik tombol di bawah untuk kembali ke Step 1.
            </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("← Kembali ke Step 1 — Data Pasien"):
                st.session_state.step = 1
                st.rerun()
        else:
            # Ringkasan step 1
            bd = st.session_state.basic_data
            st.markdown(
                f"<div style='background:#E0F2FE;border:1px solid #BAE6FD;border-radius:14px;"
                f"padding:.8rem 1.1rem;margin-bottom:1rem;font-size:12px;color:#0C4A6E;'>"
                f"✅ <strong>Data Pasien:</strong> {bd['Age']} tahun · {bd['Gender']} · BMI {bd['BMI']} · "
                f"{bd['Smoking_Status']} · Aktivitas: {bd['Physical_Activity_Level']} · "
                f"Riwayat Jantung: {'Ada' if bd['Family_History_CVD'] else 'Tidak'} · "
                f"Riwayat DM: {'Ada' if bd['Family_History_T2D'] else 'Tidak'}"
                f"</div>",
                unsafe_allow_html=True
            )

            # ── FORM INPUT (ATAS) ──
            st.subheader("🩺 Step 2 — Data Medis & Lab")
            st.markdown("<div class='blue-line'></div><br>", unsafe_allow_html=True)

            with st.form("form_step2"):
                st.markdown("**🫀 Tekanan Darah & Jantung**")
                a1, b1, c1, d1 = st.columns(4)
                with a1:
                    sys_bp = st.number_input("Systolic BP",            0, 300, 120)
                with b1:
                    dia_bp = st.number_input("Diastolic BP",           0, 200, 80)
                with c1:
                    rhr    = st.number_input("Resting Heart Rate",     0, 250, 75)
                with d1:
                    hrv    = st.number_input("HRV",                    0, 200, 50)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("**🧪 Profil Lipid**")
                a2, b2, c2, d2 = st.columns(4)
                with a2:
                    chol = st.number_input("Cholesterol",   0.0, 600.0,  200.0, format="%.1f")
                with b2:
                    ldl  = st.number_input("LDL",           0.0, 400.0,  100.0, format="%.1f")
                with c2:
                    hdl  = st.number_input("HDL",           0.0, 200.0,   50.0, format="%.1f")
                with d2:
                    trig = st.number_input("Triglycerides", 0.0, 1000.0, 150.0, format="%.1f")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("**🩸 Metabolik & Gula Darah**")
                a3, b3, c3, d3 = st.columns(4)
                with a3:
                    gluc  = st.number_input("Glucose Level", 0.0, 600.0,  90.0, format="%.1f")
                with b3:
                    hba1c = st.number_input("HbA1c (%)",     0.0,  20.0,   5.0, format="%.1f")
                with c3:
                    crp   = st.number_input("CRP",           0.0, 100.0,   1.0, format="%.2f")
                with d3:
                    egfr  = st.number_input("eGFR",          0.0, 200.0,  90.0, format="%.1f")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("**🧬 Data Genomik**")
                a4, b4, c4, d4 = st.columns(4)
                with a4:
                    prs_c = st.number_input("PRS Cardiometabolic",  value=0.0, format="%.4f")
                with b4:
                    prs_d = st.number_input("PRS Type2Diabetes",    value=0.0, format="%.4f")
                with c4:
                    apoe  = st.selectbox("APOE e4 Carrier",         [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")
                with d4:
                    brca  = st.selectbox("BRCA Pathogenic Variant", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")

                st.markdown("<br>", unsafe_allow_html=True)
                bc1, bc2, bc3 = st.columns([4, 2, 2])
                with bc1:
                    submitted2 = st.form_submit_button("🔍 Prediksi Sekarang", use_container_width=True)
                with bc3:
                    back_btn = st.form_submit_button("← Kembali ke Step 1", use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

            if back_btn:
                st.session_state.step = 1
                st.rerun()

            # ── PROSES PREDIKSI ──
            if submitted2:
                med = {
                    "Cholesterol": chol, "Glucose_Level": gluc, "HbA1c": hba1c,
                    "PRS_Cardiometabolic": prs_c, "PRS_Type2Diabetes": prs_d,
                    "APOE_e4_Carrier": apoe, "BRCA_Pathogenic_Variant": brca,
                    "Resting_Heart_Rate": rhr, "HRV": hrv,
                    "Systolic_BP": sys_bp, "Diastolic_BP": dia_bp,
                    "LDL": ldl, "HDL": hdl, "Triglycerides": trig,
                    "CRP": crp, "eGFR": egfr,
                }
                full_data = {**st.session_state.basic_data, **med}
                input_df  = pd.DataFrame([full_data])[expected_columns]

                with st.spinner("Menganalisis data pasien..."):
                    pred     = model.predict(input_df)
                    heart    = label_mapping[pred[0][0]]
                    diabetes = label_mapping[pred[0][1]]

                    supabase.table("data_pasien").insert({
                        "age":                  st.session_state.basic_data["Age"],
                        "gender":               st.session_state.basic_data["Gender"],
                        "bmi":                  st.session_state.basic_data["BMI"],
                        "smoking_status":       st.session_state.basic_data["Smoking_Status"],
                        "alcohol_consumption":  st.session_state.basic_data["Alcohol_Consumption"],
                        "physical_activity":    st.session_state.basic_data["Physical_Activity_Level"],
                        "sleep_hours":          st.session_state.basic_data["Sleep_Hours"],
                        "stress_level":         st.session_state.basic_data["Stress_Level"],
                        "waist_circumference":  st.session_state.basic_data["Waist_Circumference"],
                    }).execute()

                    supabase.table("hasil_prediksi").insert({
                        "heart_risk": heart, "diabetes_risk": diabetes
                    }).execute()

                    supabase.table("medical_data").insert({
                        "cholesterol":       chol,
                        "glucose_level":     gluc,
                        "hba1c":             hba1c,
                        "systolic_bp":       sys_bp,
                        "diastolic_bp":      dia_bp,
                        "resting_heart_rate": rhr,
                        "ldl":               ldl,
                        "hdl":               hdl,
                        "triglycerides":     trig,
                    }).execute()

                st.session_state.last_pred = (heart, diabetes, med)

            # ── HASIL PREDIKSI (BAWAH) ──
            if st.session_state.last_pred:
                h_p, d_p, med = st.session_state.last_pred
                bd = st.session_state.basic_data

                st.subheader("📊 Hasil Prediksi Risiko")
                st.markdown("<div class='blue-line'></div><br>", unsafe_allow_html=True)

                show_result_panel(h_p, d_p)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='font-size:10px;font-weight:700;letter-spacing:.09em;"
                    "text-transform:uppercase;color:#60A5FA;margin:0 0 .6rem;'>📋 Ringkasan Pasien</p>",
                    unsafe_allow_html=True
                )

                g1, g2, g3, g4, g5, g6, g7, g8 = st.columns(8)
                for col, label, val in [
                    (g1, "Umur",        f"{bd['Age']} thn"),
                    (g2, "Gender",      bd["Gender"]),
                    (g3, "BMI",         str(bd["BMI"])),
                    (g4, "TD",          f"{med['Systolic_BP']}/{med['Diastolic_BP']}"),
                    (g5, "Cholesterol", str(med["Cholesterol"])),
                    (g6, "Glucose",     str(med["Glucose_Level"])),
                    (g7, "HbA1c",       f"{med['HbA1c']}%"),
                    (g8, "Model",       model_choice),
                ]:
                    col.markdown(
                        f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;"
                        f"padding:.55rem .5rem;text-align:center;'>"
                        f"<div style='font-size:9px;color:#64748B;'>{label}</div>"
                        f"<div style='font-size:12px;font-weight:700;color:#1E293B;'>{val}</div></div>",
                        unsafe_allow_html=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)
# ==========================
# CSV MODE
# ==========================

elif input_method == "Upload CSV":
    st.subheader("📂 Upload Data Pasien (CSV)")
    st.markdown("<div class='blue-line'></div><br>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload File CSV", type=["csv"])

    st.markdown(
        "<div class='info-box'>📄 Upload file CSV berisi data pasien untuk melakukan prediksi massal secara otomatis menggunakan AI.</div>",
        unsafe_allow_html=True,
    )

    if uploaded:
        try:
            df_input = pd.read_csv(uploaded)
            missing = [c for c in expected_columns if c not in df_input.columns]
            extra   = [c for c in df_input.columns  if c not in expected_columns]
            ok = not missing

            ok_bg  = "#EAF3DE" if ok else "#FCEBEB"
            ok_bd  = "#97C459" if ok else "#F09595"
            ok_tx  = "#27500A" if ok else "#791F1F"
            ok_val = "✓" if ok else "!"
            ok_lbl = "Format valid" if ok else f"{len(missing)} kolom kurang"

            st.markdown(
                f"<div style='display:flex;gap:8px;margin:.8rem 0 .5rem;'>"
                f"<div style='background:#EFF6FF;border:0.5px solid #BFDBFE;border-radius:8px;padding:.65rem .9rem;text-align:center;min-width:80px;'>"
                f"<div style='font-size:16px;font-weight:700;color:#1E3A5F;'>{len(df_input)}</div>"
                f"<div style='font-size:10px;color:#64748B;margin-top:1px;'>Pasien</div></div>"
                f"<div style='background:#EFF6FF;border:0.5px solid #BFDBFE;border-radius:8px;padding:.65rem .9rem;text-align:center;min-width:80px;'>"
                f"<div style='font-size:16px;font-weight:700;color:#1E3A5F;'>{len(df_input.columns)}</div>"
                f"<div style='font-size:10px;color:#64748B;margin-top:1px;'>Kolom</div></div>"
                f"<div style='background:{ok_bg};border:0.5px solid {ok_bd};border-radius:8px;padding:.65rem .9rem;text-align:center;min-width:95px;'>"
                f"<div style='font-size:16px;font-weight:700;color:{ok_tx};'>{ok_val}</div>"
                f"<div style='font-size:10px;color:{ok_tx};margin-top:1px;'>{ok_lbl}</div></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

            if missing:
                st.error("Kolom kurang: " + ", ".join(f"`{c}`" for c in missing))
            else:
                if extra:
                    st.info(f"{len(extra)} kolom tambahan tidak digunakan untuk prediksi.")

                if st.button("🚀 Jalankan Prediksi"):
                    with st.spinner("Memproses data pasien..."):
                        preds = model.predict(df_input[expected_columns])

                    df_res = df_input.copy()
                    df_res["Heart_Disease_Risk"] = [label_mapping[p[0]] for p in preds]
                    df_res["Diabetes_Risk"]       = [label_mapping[p[1]] for p in preds]
                    df_res["Kesimpulan"] = [
                        sentence(label_mapping[p[0]], label_mapping[p[1]])
                        .replace("<strong>", "").replace("</strong>", "")
                        for p in preds
                    ]
                    df_res["Rekomendasi"] = [
                        " | ".join(recs(label_mapping[p[0]], label_mapping[p[1]]))
                        for p in preds
                    ]

                    # Simpan ke Supabase
                    for _, row in df_res.iterrows():
                        supabase.table("hasil_prediksi").insert({
                            "heart_risk": row["Heart_Disease_Risk"],
                            "diabetes_risk": row["Diabetes_Risk"],
                        }).execute()

                    hc = df_res["Heart_Disease_Risk"].value_counts()
                    dc = df_res["Diabetes_Risk"].value_counts()

                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;'>📊 Distribusi Risiko</p>", unsafe_allow_html=True)

                    cs6 = st.columns(6)
                    for col, lbl, val, risk in [
                        (cs6[0], "Jantung Tinggi",  hc.get("High", 0),     "High"),
                        (cs6[1], "Jantung Sedang",  hc.get("Moderate", 0), "Moderate"),
                        (cs6[2], "Jantung Rendah",  hc.get("Low", 0),      "Low"),
                        (cs6[3], "Diabetes Tinggi", dc.get("High", 0),     "High"),
                        (cs6[4], "Diabetes Sedang", dc.get("Moderate", 0), "Moderate"),
                        (cs6[5], "Diabetes Rendah", dc.get("Low", 0),      "Low"),
                    ]:
                        r = RISK[risk]
                        col.markdown(
                            f"<div style='background:{r['bg']};border:0.5px solid {r['bd']};"
                            f"border-radius:8px;padding:.6rem .4rem;text-align:center;'>"
                            f"<div style='font-size:15px;font-weight:700;color:{r['tx']};'>{val}</div>"
                            f"<div style='font-size:10px;color:{r['tx']};opacity:.85;margin-top:2px;"
                            f"line-height:1.3;'>{lbl}</div></div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;'>👥 Hasil Per Pasien</p>", unsafe_allow_html=True)

                    for idx, row in df_res.iterrows():
                        name = row.get("Patient_ID", row.get("Nama", row.get("Name", f"Pasien #{idx + 1}")))
                        hr_r = row["Heart_Disease_Risk"]
                        dr_r = row["Diabetes_Risk"]
                        with st.expander(f"{name}  ·  Jantung: {RISK[hr_r]['label']}  ·  Diabetes: {RISK[dr_r]['label']}"):
                            show_result_panel(hr_r, dr_r)

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
        <div style='font-size:32px;margin-bottom:8px;'>📁</div>
        <p style='font-size:14px;color:#1447B4;font-weight:700;margin:0;'>Upload file CSV untuk memulai</p>
        <p style='font-size:12px;color:#93C5FD;margin:5px 0 0;'>Pastikan format kolom sesuai dengan 32 kolom yang dibutuhkan</p>
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