import streamlit as st


# ==========================
# SIDEBAR
# ==========================
def render_sidebar(rf_model, xgb_model):
    with st.sidebar:
        st.markdown(
            """
            <div style='text-align:center;margin-bottom:2rem;'>
            <div style='font-size:55px;'>🩺</div>
            <div style='font-size:28px;font-weight:800;color:white;margin-top:-10px;'>MediRisk</div>
            <div style='font-size:12px;color:#EFF6FF;margin-top:3px;'>AI Healthcare Dashboard</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### ⚙ Pengaturan Sistem")
        st.markdown("""
            <style>
                div[data-baseweb="select"] input {
                pointer-events: none !important;
                caret-color: transparent !important;
                }
            </style>
         """, unsafe_allow_html=True)
        
        model_choice = st.selectbox(
            "Pilih Model",
            ["Multivariate Random Forest", "XGBoost"],
            accept_new_options=False,
        )
        model = rf_model if model_choice == "Multivariate Random Forest" else xgb_model
        input_method = st.radio("Mode Input", ["Isi Manual", "Upload CSV"])

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="background:rgba(255,255,255,.18);padding:1rem;border-radius:16px;border:1px solid rgba(255,255,255,.22);">
            <div style="color:white;font-size:14px;font-weight:700;margin-bottom:10px;">📌 Informasi</div>
            <div style="color:#F8FAFC;font-size:12px;line-height:1.8;">
            Sistem membantu screening awal risiko kesehatan pasien menggunakan AI.<br><br>
            ⚠️ Hasil bukan pengganti diagnosis dokter.
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return model_choice, model, input_method
