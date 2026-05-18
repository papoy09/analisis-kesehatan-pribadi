import streamlit as st


def render_info_bar():
    info1, info2, info3, info4 = st.columns(4)

    with info1:
        st.markdown(
            "<div class='metric-card'><div class='metric-title'>🧠 AI Engine</div><div class='metric-value'>2</div><span class='badge-success'>Random Forest + XGBoost</span></div>",
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
    with info4:
        st.markdown(
            "<div class='metric-card'><div class='metric-title'>🟢 Status</div><div class='metric-value'>100%</div><span class='badge-success'>System Online</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.markdown(
            "<div class='small-card'><div class='small-number'>98%</div><div class='small-text'>AI Accuracy</div></div>",
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            "<div class='small-card'><div class='small-number'>24/7</div><div class='small-text'>Monitoring</div></div>",
            unsafe_allow_html=True,
        )
    with e3:
        st.markdown(
            "<div class='small-card'><div class='small-number'>AI</div><div class='small-text'>Medical Support</div></div>",
            unsafe_allow_html=True,
        )
    with e4:
        st.markdown(
            "<div class='small-card'><div class='small-number'>Fast</div><div class='small-text'>Prediction Engine</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
