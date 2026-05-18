import streamlit as st

from config.risk_config import RISK, RISK_TEXT

# ==========================
# RISK HELPERS
# ==========================


def sentence(h, d):
    s = (
        f"Pasien diprediksi memiliki risiko jantung kategori <strong>{RISK_TEXT[h]}</strong>"
        f" dan diabetes kategori <strong>{RISK_TEXT[d]}</strong>."
    )
    extra = {
        (
            "High",
            "High",
        ): " Kedua risiko tinggi — segera konsultasikan dengan dokter untuk pemeriksaan menyeluruh.",
        (
            "High",
            "Moderate",
        ): " Prioritaskan pemeriksaan kardiovaskular dan kendalikan pola makan serta gula darah.",
        (
            "High",
            "Low",
        ): " Fokus pada pemeriksaan jantung: tekanan darah, kolesterol, dan kondisi kardiovaskular.",
        (
            "Moderate",
            "High",
        ): " Prioritaskan pemeriksaan gula darah (HbA1c) dan tetap jaga faktor risiko jantung.",
        (
            "Low",
            "High",
        ): " Lakukan pemeriksaan gula darah segera dan konsultasikan pola hidup ke tenaga kesehatan.",
        (
            "Moderate",
            "Moderate",
        ): " Perubahan gaya hidup sekarang dapat mencegah kedua risiko meningkat.",
        (
            "Moderate",
            "Low",
        ): " Jaga tekanan darah, kolesterol, dan tingkatkan aktivitas fisik secara rutin.",
        (
            "Low",
            "Moderate",
        ): " Kurangi konsumsi gula, jaga berat badan ideal, dan rutin berolahraga.",
        (
            "Low",
            "Low",
        ): " Pertahankan gaya hidup sehat dan lakukan pemeriksaan rutin secara berkala.",
    }
    return s + extra.get((h, d), "")


def recs(h, d):
    base = [
        "Terapkan pola makan seimbang — perbanyak sayur dan serat; kurangi gula, garam, dan lemak jenuh.",
        "Olahraga minimal 150 menit per minggu — jalan kaki, bersepeda, atau berenang.",
        "Jaga berat badan ideal, tidur 7–9 jam, dan kelola stres dengan baik.",
        "Hindari merokok dan batasi konsumsi alkohol.",
    ]
    base.append(
        {
            "Low": "Risiko jantung rendah — pertahankan tekanan darah dan kolesterol dalam batas normal.",
            "Moderate": "Risiko jantung sedang — pantau tekanan darah dan kolesterol berkala, kurangi garam dan lemak.",
            "High": "Risiko jantung tinggi — segera konsultasikan dengan dokter spesialis jantung.",
        }[h]
    )
    base.append(
        {
            "Low": "Risiko diabetes rendah — pertahankan pola makan sehat dan berat badan ideal.",
            "Moderate": "Risiko diabetes sedang — kurangi minuman manis, pantau gula darah secara berkala.",
            "High": "Risiko diabetes tinggi — segera lakukan pemeriksaan gula darah puasa dan HbA1c bersama dokter.",
        }[d]
    )
    extra_map = {
        (
            "High",
            "High",
        ): "Dengan kedua risiko tinggi, jangan tunda pemeriksaan medis lanjutan.",
        (
            "Moderate",
            "Moderate",
        ): "Perubahan gaya hidup sekarang lebih mudah daripada pengobatan di kemudian hari.",
        (
            "Low",
            "Low",
        ): "Jadikan pemeriksaan tahunan sebagai kebiasaan, terutama jika ada riwayat keluarga.",
    }
    if (h, d) in extra_map:
        base.append(extra_map[(h, d)])
    return base


def show_result_panel(h, d):
    hr, dr = RISK[h], RISK[d]
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
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='border-left:3px solid #60A5FA;padding:.7rem 1rem;background:#E6F1FB;"
        f"border-radius:0 10px 10px 0;font-size:13px;color:#042C53;line-height:1.7;margin-bottom:1rem;'>"
        f"{sentence(h, d)}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size:10px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;"
        "color:#60A5FA;margin:0 0 .6rem;'>💡 Rekomendasi Kesehatan</p>",
        unsafe_allow_html=True,
    )
    for i, r in enumerate(recs(h, d), 1):
        st.markdown(
            f"<div style='display:flex;gap:10px;align-items:flex-start;padding:.55rem .85rem;"
            f"border:1px solid #DBEAFE;border-radius:10px;margin-bottom:5px;background:#F8FCFF;'>"
            f"<span style='flex-shrink:0;width:20px;height:20px;border-radius:50%;background:#DBEAFE;"
            f"color:#1447B4;font-size:10px;font-weight:700;display:flex;align-items:center;"
            f"justify-content:center;margin-top:1px;'>{i}</span>"
            f"<p style='font-size:12px;color:#334155;line-height:1.6;margin:0;'>{r}</p></div>",
            unsafe_allow_html=True,
        )
