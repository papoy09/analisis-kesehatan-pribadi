import streamlit as st
import pandas as pd
import time

from config.constant import *
from utils.risk_helper import *

# ==========================
# CSV MODE
# ==========================


def render_upload_csv(supabase, model):
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
            extra = [c for c in df_input.columns if c not in expected_columns]
            ok = not missing

            ok_bg = "#EAF3DE" if ok else "#FCEBEB"
            ok_bd = "#97C459" if ok else "#F09595"
            ok_tx = "#27500A" if ok else "#791F1F"
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
                    st.info(
                        f"{len(extra)} kolom tambahan tidak digunakan untuk prediksi."
                    )

                if st.button("🚀 Jalankan Prediksi"):
                    with st.spinner("Memproses data pasien..."):
                        preds = model.predict(df_input[expected_columns])

                    df_res = df_input.copy()
                    df_res["Heart_Disease_Risk"] = [label_mapping[p[0]] for p in preds]
                    df_res["Diabetes_Risk"] = [label_mapping[p[1]] for p in preds]
                    df_res["Kesimpulan"] = [
                        sentence(label_mapping[p[0]], label_mapping[p[1]])
                        .replace("<strong>", "")
                        .replace("</strong>", "")
                        for p in preds
                    ]
                    df_res["Rekomendasi"] = [
                        " | ".join(recs(label_mapping[p[0]], label_mapping[p[1]]))
                        for p in preds
                    ]

                    # ── Simpan ke Supabase Storage ──
                    original_bytes = df_input.to_csv(index=False).encode("utf-8")
                    result_bytes = df_res.to_csv(index=False).encode("utf-8")
                    result_name = f"hasil_prediksi_{int(time.time())}.csv"

                    supabase.storage.from_("csv-files").upload(
                        path=uploaded.name,
                        file=original_bytes,
                        file_options={"content-type": "text/csv"},
                    )
                    supabase.storage.from_("csv-files").upload(
                        path=result_name,
                        file=result_bytes,
                        file_options={"content-type": "text/csv"},
                    )
                    supabase.table("uploaded-files").insert(
                        {
                            "filename": uploaded.name,
                            "storage_path": f"csv-files/{uploaded.name}",
                        }
                    ).execute()

                    # ── Simpan hasil per baris ke Supabase DB ──
                    for _, row in df_res.iterrows():
                        supabase.table("hasil_prediksi").insert(
                            {
                                "heart_risk": row["Heart_Disease_Risk"],
                                "diabetes_risk": row["Diabetes_Risk"],
                            }
                        ).execute()

                    st.success("File CSV berhasil disimpan ke Storage!")

                    hc = df_res["Heart_Disease_Risk"].value_counts()
                    dc = df_res["Diabetes_Risk"].value_counts()

                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(
                        "<p style='font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;'>📊 Distribusi Risiko</p>",
                        unsafe_allow_html=True,
                    )

                    cs6 = st.columns(6)
                    for col, lbl, val, risk in [
                        (cs6[0], "Jantung Tinggi", hc.get("High", 0), "High"),
                        (cs6[1], "Jantung Sedang", hc.get("Moderate", 0), "Moderate"),
                        (cs6[2], "Jantung Rendah", hc.get("Low", 0), "Low"),
                        (cs6[3], "Diabetes Tinggi", dc.get("High", 0), "High"),
                        (cs6[4], "Diabetes Sedang", dc.get("Moderate", 0), "Moderate"),
                        (cs6[5], "Diabetes Rendah", dc.get("Low", 0), "Low"),
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
                    st.markdown(
                        "<p style='font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;'>👥 Hasil Per Pasien</p>",
                        unsafe_allow_html=True,
                    )

                    for idx, row in df_res.iterrows():
                        name = row.get(
                            "Patient_ID",
                            row.get("Nama", row.get("Name", f"Pasien #{idx + 1}")),
                        )
                        hr_r = row["Heart_Disease_Risk"]
                        dr_r = row["Diabetes_Risk"]
                        with st.expander(
                            f"{name}  ·  Jantung: {RISK[hr_r]['label']}  ·  Diabetes: {RISK[dr_r]['label']}"
                        ):
                            show_result_panel(hr_r, dr_r)

                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Download Hasil CSV",
                        result_bytes,
                        "hasil_prediksi.csv",
                        "text/csv",
                    )

        except Exception as e:
            st.error("Error memproses file.")
            st.exception(e)

        else:
            st.markdown(
                """
                <div style='border:1px dashed #93C5FD;border-radius:18px;padding:2.5rem;
                text-align:center;background:#EFF6FF;margin-top:1rem;'>
                <div style='font-size:32px;margin-bottom:8px;'>📁</div>
                <p style='font-size:14px;color:#1447B4;font-weight:700;margin:0;'>Upload file CSV untuk memulai</p>
                <p style='font-size:12px;color:#93C5FD;margin:5px 0 0;'>Pastikan format kolom sesuai dengan 32 kolom yang dibutuhkan</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)
