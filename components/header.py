import streamlit as st

# ==========================
# HEADER
# ==========================


def render_header():
    st.markdown(
        """
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
""",
        unsafe_allow_html=True,
    )
