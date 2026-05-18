from supabase import create_client
from dotenv import load_dotenv

from components.header import render_header
from components.info_bar import render_info_bar
from components.sidebar import *
from components.bottom_section import render_buttom_section
from components.footer import render_footer
from assets.styles import *

from config.constant import *
from config.risk_config import *

from models.model_loader import *

from views.manual_input import *
from views.upload_csv import *

import os
import streamlit as st

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
#  assets/styles.py
load_css()

# # ==========================
# # HEADER
# # ==========================
# components.header.py
render_header()

# ==========================
# INFO BAR
# ==========================
# components/infobar.py
render_info_bar()

# ==========================
# MODEL
# ==========================
# models/model_loader.py
# config/constant.py

# ==========================
# RISK HELPERS
# ==========================
# utils/risk_helper.py

# ==========================
# SIDEBAR
# ==========================
# components/sidebar.py
model_choice, model, input_method = render_sidebar(rf_model, xgb_model)

# ==========================
# SESSION STATE
# ==========================

for k in ["basic_data", "step", "last_pred"]:
    if k not in st.session_state:
        st.session_state[k] = {} if k == "basic_data" else (1 if k == "step" else None)

# ==========================
# MANUAL INPUT
# ==========================
# pages/isi_manual.py
if input_method == "Isi Manual":
    render_manual_input(model, model_choice, supabase)

# ==========================
# CSV MODE
# ==========================
# pages/upload_csv.py
elif input_method == "Upload CSV":
    render_upload_csv(supabase, model)

# ==========================
# BOTTOM SECTION
# ==========================
# components/bottom_section.py
render_buttom_section()

# ==========================
# FOOTER
# ==========================
# components/footer.py
render_footer()
