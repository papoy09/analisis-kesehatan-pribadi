import streamlit as st

# ==========================
# BOTTOM SECTION
# ==========================


def render_buttom_section():
    st.markdown("<br>", unsafe_allow_html=True)
    bx1, bx2, bx3 = st.columns(3)
    with bx1:
        st.markdown(
            "<div class='soft-card'><h3>🫀 Cardio Risk</h3><p style='font-size:13px;color:#64748B;line-height:1.8;'>Pemeriksaan dini membantu mengurangi risiko penyakit jantung dan komplikasi kesehatan.</p></div>",
            unsafe_allow_html=True,
        )
    with bx2:
        st.markdown(
            "<div class='soft-card'><h3>🩸 Diabetes Care</h3><p style='font-size:13px;color:#64748B;line-height:1.8;'>Monitoring kadar gula darah secara rutin membantu menjaga kondisi tubuh tetap stabil.</p></div>",
            unsafe_allow_html=True,
        )
    with bx3:
        st.markdown(
            "<div class='soft-card'><h3>⚡ AI Technology</h3><p style='font-size:13px;color:#64748B;line-height:1.8;'>Machine learning meningkatkan kecepatan dan efisiensi analisis data kesehatan pasien.</p></div>",
            unsafe_allow_html=True,
        )
