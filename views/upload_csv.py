import streamlit as st
import pandas as pd
import time

from config.constant import expected_columns, label_mapping
from config.risk_config import RISK
from utils.risk_helper import sentence, recs, show_result_panel


def render_upload_csv(supabase, model):
    st.subheader("📂 Upload Data Pasien (CSV)")
    st.markdown("<div class='blue-line'></div><br>", unsafe_allow_html=True)

    if "csv_file" not in st.session_state:
        st.session_state["csv_file"] = None

    # ── Drop zone / upload area ──────────────────────────────────────────────
    uploaded = st.file_uploader(
        "Drag & drop file CSV di sini, atau klik untuk pilih file",
        type=["csv"],
        label_visibility="visible",
    )

    if uploaded is None:
        st.session_state["csv_file"] = None
        st.markdown(
            """
            <div style="
                border: 1.5px dashed #CBD5E1;
                border-radius: 12px;
                background: #F8FAFC;
                padding: 2.2rem 2rem;
                text-align: center;
                margin-top: -1rem;
            ">
                <div style="font-size:13px;color:#94A3B8;margin-top:6px;">
                    Format yang didukung: <code>.csv</code> &nbsp;·&nbsp; 32 kolom dibutuhkan
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── File preview panel ───────────────────────────────────────────────────
    try:
        df_input = pd.read_csv(uploaded)
    except Exception as e:
        st.error("Gagal membaca file CSV.")
        st.exception(e)
        return

    n_rows = len(df_input)
    n_cols = len(df_input.columns)
    missing = [c for c in expected_columns if c not in df_input.columns]
    extra = [c for c in df_input.columns if c not in expected_columns]
    is_valid = not missing

    file_kb = round(uploaded.size / 1024, 1)
    file_size_str = f"{file_kb} KB" if file_kb < 1024 else f"{round(file_kb/1024,1)} MB"


    # file header card
    # file header card
    with st.container(border=True):
        col_icon, col_info = st.columns([0.06, 0.94])
        with col_icon:
            st.markdown("📄")
        with col_info:
            st.markdown(f"**{uploaded.name}**")
            st.caption(file_size_str)

        c1, c2, c3 = st.columns(3)
        c1.metric("Baris pasien", f"{n_rows:,}")
        c2.metric("Kolom", n_cols)
        c3.metric("Format", "✓ Valid" if is_valid else f"✗ {len(missing)} kurang")

        if missing:
            st.error(f"⚠ Kolom yang kurang: {', '.join(missing)}")
        elif extra:
            st.info(f"{len(extra)} kolom tambahan tidak digunakan untuk prediksi.")

    

    # ── Run button ───────────────────────────────────────────────────────────
    if not is_valid:
        st.button("Jalankan Prediksi", disabled=True, use_container_width=True)
        return

    if not st.button("Jalankan Prediksi", use_container_width=True, type="primary"):
        return

    # ── Prediction ───────────────────────────────────────────────────────────
    with st.spinner("Memproses data pasien..."):
        preds = model.predict(df_input[expected_columns])

    df_res = df_input.copy()
    df_res["Heart_Disease_Risk"] = [label_mapping[p[0]] for p in preds]
    df_res["Diabetes_Risk"]      = [label_mapping[p[1]] for p in preds]
    df_res["Kesimpulan"] = [
        sentence(label_mapping[p[0]], label_mapping[p[1]])
        .replace("<strong>", "").replace("</strong>", "")
        for p in preds
    ]
    df_res["Rekomendasi"] = [
        " | ".join(recs(label_mapping[p[0]], label_mapping[p[1]])) for p in preds
    ]

    original_bytes = df_input.to_csv(index=False).encode("utf-8")
    result_bytes   = df_res.to_csv(index=False).encode("utf-8")
    result_name    = f"hasil_prediksi_{int(time.time())}.csv"

    # ── Cek duplikat filename di Supabase ────────────────────────────────────
    existing = supabase.table("uploaded-files").select("filename").eq("filename", uploaded.name).execute()

    if existing.data:
        st.warning(
            f"⚠️ File dengan nama **{uploaded.name}** sudah pernah diupload sebelumnya. "
            "Silakan ganti nama file terlebih dahulu sebelum mengupload ulang."
        )
        return

    # ── Upload ke Supabase (hanya kalau nama belum ada) ──────────────────────
    supabase.storage.from_("csv-files").upload(
        path=uploaded.name, file=original_bytes,
        file_options={"content-type": "text/csv"},
    )
    supabase.storage.from_("csv-files").upload(
        path=result_name, file=result_bytes,
        file_options={"content-type": "text/csv"},
    )
    supabase.table("uploaded-files").insert({
        "filename": uploaded.name,
        "storage_path": f"csv-files/{uploaded.name}",
    }).execute()

    for _, row in df_res.iterrows():
        supabase.table("hasil_prediksi").insert({
            "heart_risk": row["Heart_Disease_Risk"],
            "diabetes_risk": row["Diabetes_Risk"],
        }).execute()

    st.success("File CSV berhasil disimpan ke Storage!")

    # ── Distribusi risiko ────────────────────────────────────────────────────
    hc = df_res["Heart_Disease_Risk"].value_counts()
    dc = df_res["Diabetes_Risk"].value_counts()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:10px;font-weight:700;letter-spacing:.08em;"
        "text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;'>📊 Distribusi Risiko</p>",
        unsafe_allow_html=True,
    )

    cs6 = st.columns(6)
    for col, lbl, val, risk in [
        (cs6[0], "Jantung Tinggi",   hc.get("High", 0),     "High"),
        (cs6[1], "Jantung Sedang",   hc.get("Moderate", 0), "Moderate"),
        (cs6[2], "Jantung Rendah",   hc.get("Low", 0),      "Low"),
        (cs6[3], "Diabetes Tinggi",  dc.get("High", 0),     "High"),
        (cs6[4], "Diabetes Sedang",  dc.get("Moderate", 0), "Moderate"),
        (cs6[5], "Diabetes Rendah",  dc.get("Low", 0),      "Low"),
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

    # ── Hasil per pasien ─────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:10px;font-weight:700;letter-spacing:.08em;"
        "text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;'>👥 Hasil Per Pasien</p>",
        unsafe_allow_html=True,
    )

    for idx, row in df_res.iterrows():
        name = row.get("Patient_ID", row.get("Nama", row.get("Name", f"Pasien #{idx + 1}")))
        hr_r = row["Heart_Disease_Risk"]
        dr_r = row["Diabetes_Risk"]
        with st.container(border=True):
            st.markdown(f"**{name}**  ·  Jantung: {RISK[hr_r]['label']}  ·  Diabetes: {RISK[dr_r]['label']}")
            show_result_panel(hr_r, dr_r)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.download_button(
        "⬇ Download Hasil CSV",
        result_bytes,
        "hasil_prediksi.csv",
        "text/csv",
        use_container_width=True,
    )