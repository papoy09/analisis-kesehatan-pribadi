import streamlit as st


def render_info_bar():
    info1, info2, info3 = st.columns(3)

    with info1:
        st.markdown(
            "<div class='metric-card'><div class='metric-title'>🧠 AI Engine</div><div class='metric-value'>2</div><span class='badge-success'>Multivariate Random Forest + XGBoost</span></div>",
            unsafe_allow_html=True,
        )
    with info2:
        st.markdown(
            "<div class='metric-card'><div class='metric-title'>📊 Parameters</div><div class='metric-value'>32</div><span class='badge-warning'>Clinical Features</span></div>",
            unsafe_allow_html=True,
        )
    with info3:
        st.markdown(
            "<div class='metric-card'><div class='metric-title'>⚡ Prediction</div><div class='metric-value'>Dual</div><span class='badge-success'>Heart + Diabetes</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    