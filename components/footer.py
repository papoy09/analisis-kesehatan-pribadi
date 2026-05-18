import streamlit as st

# ==========================
# FOOTER
# ==========================


def render_footer():
    st.markdown(
        """
    <div style="margin-top:2rem;padding:1.4rem;text-align:center;
    background:rgba(255,255,255,.90);border-radius:20px;
    border:1px solid rgba(191,219,254,.8);backdrop-filter:blur(10px);
    font-size:12px;color:#64748B;">
    <div style="font-size:18px;font-weight:800;color:#2563EB;margin-bottom:5px;">🩺 MediRisk AI</div>
    Clinical Decision Support System<br>
    Designed for early heart disease & diabetes risk screening
    </div>
    """,
        unsafe_allow_html=True,
    )
