import streamlit as st
import pandas as pd

from utils.risk_helper import *
from config.constant import *

# ==========================
# MANUAL INPUT
# ==========================


def render_manual_input(model, model_choice, supabase):
    step = st.session_state.step

    step1_class = "step-active" if step == 1 else "step-done"
    step2_class = (
        "step-active" if step == 2 else ("step-inactive" if step == 1 else "step-done")
    )
    st.markdown(
        f"<div class='step-bar'>"
        f"<div class='{step1_class}'>{'✓ ' if step > 1 else ''}1 · Data Pasien</div>"
        f"<div class='{step2_class}'>2 · Data Medis & Prediksi</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── STEP 1 ──────────────────────────────────────────────────────────
    if step == 1:
        st.subheader("📋 Step 1 — Data Pasien")
        st.markdown("<div class='blue-line'></div><br>", unsafe_allow_html=True)

        with st.form("form_step1"):
            st.markdown("**🧍 Informasi Dasar**")
            col1, col2, col3 = st.columns(3)
            with col1:
                age = st.number_input("Umur (tahun)", 1, 120, 30)
                gender = st.selectbox("Gender", ["Male", "Female"])
                bmi = st.number_input("BMI", 0.0, 80.0, 22.0, format="%.1f")
            with col2:
                smoking = st.selectbox(
                    "Smoking Status", ["Non-smoker", "Former smoker", "Current smoker"]
                )
                alcohol = st.selectbox(
                    "Alcohol Consumption", ["Low", "Moderate", "High"]
                )
                activity = st.selectbox(
                    "Physical Activity",
                    ["Sedentary", "Lightly Active", "Moderately Active", "Active"],
                )
            with col3:
                diet = st.selectbox(
                    "Diet Type", ["Balanced", "Unhealthy", "Vegetarian", "High-protein"]
                )
                waist = st.number_input(
                    "Waist Circumference (cm)", 0.0, 200.0, 80.0, format="%.1f"
                )

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("**😴 Gaya Hidup & Psikososial**")
            c1, c2, c3 = st.columns(3)
            with c1:
                sleep_h = st.number_input(
                    "Sleep Hours / hari", 0.0, 24.0, 7.0, format="%.1f"
                )
                sleep_q = st.selectbox(
                    "Sleep Quality", ["Poor", "Fair", "Good", "Excellent"]
                )
            with c2:
                stress = st.number_input(
                    "Stress Level (0–10)", 0.0, 10.0, 5.0, format="%.1f"
                )
                depress = st.number_input("Depression Score", 0, value=0)
            with c3:
                anxiety = st.number_input("Anxiety Score", 0, value=0)
                social = st.number_input("Social Isolation Index", 0, value=0)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("**🧬 Riwayat Keluarga**")
            f1, f2 = st.columns(2)
            with f1:
                fam_cvd = st.selectbox(
                    "Riwayat Jantung dalam Keluarga",
                    [0, 1],
                    format_func=lambda x: "Tidak Ada" if x == 0 else "Ada",
                )
            with f2:
                fam_t2d = st.selectbox(
                    "Riwayat Diabetes dalam Keluarga",
                    [0, 1],
                    format_func=lambda x: "Tidak Ada" if x == 0 else "Ada",
                )

            st.markdown("<br>", unsafe_allow_html=True)
            submitted1 = st.form_submit_button("Simpan & Lanjut ke Data Medis →")

        if submitted1:
            st.session_state.basic_data = {
                "Age": age,
                "Gender": gender,
                "BMI": bmi,
                "Smoking_Status": smoking,
                "Alcohol_Consumption": alcohol,
                "Physical_Activity_Level": activity,
                "Diet_Type": diet,
                "Waist_Circumference": waist,
                "Sleep_Hours": sleep_h,
                "Sleep_Quality": sleep_q,
                "Stress_Level": stress,
                "Depression_Score": depress,
                "Anxiety_Score": anxiety,
                "Social_Isolation_Index": social,
                "Family_History_CVD": fam_cvd,
                "Family_History_T2D": fam_t2d,
            }
            st.session_state.step = 2
            st.session_state.last_pred = None
            st.rerun()

        if st.session_state.basic_data:
            bd = st.session_state.basic_data
            with st.expander("📄 Lihat data pasien yang sudah disimpan"):
                g1, g2, g3, g4 = st.columns(4)
                g1.markdown(
                    f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;padding:.6rem .8rem;'><div style='font-size:10px;color:#64748B;'>Umur</div><div style='font-size:14px;font-weight:700;color:#1E293B;'>{bd['Age']} tahun</div></div>",
                    unsafe_allow_html=True,
                )
                g2.markdown(
                    f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;padding:.6rem .8rem;'><div style='font-size:10px;color:#64748B;'>Gender</div><div style='font-size:14px;font-weight:700;color:#1E293B;'>{bd['Gender']}</div></div>",
                    unsafe_allow_html=True,
                )
                g3.markdown(
                    f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;padding:.6rem .8rem;'><div style='font-size:10px;color:#64748B;'>BMI</div><div style='font-size:14px;font-weight:700;color:#1E293B;'>{bd['BMI']}</div></div>",
                    unsafe_allow_html=True,
                )
                g4.markdown(
                    f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;padding:.6rem .8rem;'><div style='font-size:10px;color:#64748B;'>Merokok</div><div style='font-size:14px;font-weight:700;color:#1E293B;'>{bd['Smoking_Status']}</div></div>",
                    unsafe_allow_html=True,
                )

    # ── STEP 2 ──────────────────────────────────────────────────────────
    elif step == 2:

        if not st.session_state.basic_data:
            st.markdown(
                """
            <div style="background:#FEF3C7;border:1px solid #F59E0B;border-radius:16px;
            padding:1.2rem 1.5rem;margin-bottom:1rem;">
            <div style="font-size:15px;font-weight:700;color:#92400E;margin-bottom:6px;">
            ⚠️ Data Pasien Belum Diisi</div>
            <div style="font-size:13px;color:#78350F;line-height:1.7;">
            Anda harus mengisi <strong>Step 1 — Data Pasien</strong> terlebih dahulu.
            </div></div>
            """,
                unsafe_allow_html=True,
            )
            if st.button("← Kembali ke Step 1 — Data Pasien"):
                st.session_state.step = 1
                st.rerun()
        else:
            bd = st.session_state.basic_data
            st.markdown(
                f"<div style='background:#E0F2FE;border:1px solid #BAE6FD;border-radius:14px;"
                f"padding:.8rem 1.1rem;margin-bottom:1rem;font-size:12px;color:#0C4A6E;'>"
                f"✅ <strong>Data Pasien:</strong> {bd['Age']} tahun · {bd['Gender']} · BMI {bd['BMI']} · "
                f"{bd['Smoking_Status']} · Aktivitas: {bd['Physical_Activity_Level']} · "
                f"Riwayat Jantung: {'Ada' if bd['Family_History_CVD'] else 'Tidak'} · "
                f"Riwayat DM: {'Ada' if bd['Family_History_T2D'] else 'Tidak'}"
                f"</div>",
                unsafe_allow_html=True,
            )

            st.subheader("🩺 Step 2 — Data Medis & Lab")
            st.markdown("<div class='blue-line'></div><br>", unsafe_allow_html=True)

            with st.form("form_step2"):
                st.markdown("**🫀 Tekanan Darah & Jantung**")
                a1, b1, c1, d1 = st.columns(4)
                with a1:
                    sys_bp = st.number_input("Systolic BP", 0, 300, 120)
                with b1:
                    dia_bp = st.number_input("Diastolic BP", 0, 200, 80)
                with c1:
                    rhr = st.number_input("Resting Heart Rate", 0, 250, 75)
                with d1:
                    hrv = st.number_input("HRV", 0, 200, 50)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("**🧪 Profil Lipid**")
                a2, b2, c2, d2 = st.columns(4)
                with a2:
                    chol = st.number_input(
                        "Cholesterol", 0.0, 600.0, 200.0, format="%.1f"
                    )
                with b2:
                    ldl = st.number_input("LDL", 0.0, 400.0, 100.0, format="%.1f")
                with c2:
                    hdl = st.number_input("HDL", 0.0, 200.0, 50.0, format="%.1f")
                with d2:
                    trig = st.number_input(
                        "Triglycerides", 0.0, 1000.0, 150.0, format="%.1f"
                    )

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("**🩸 Metabolik & Gula Darah**")
                a3, b3, c3, d3 = st.columns(4)
                with a3:
                    gluc = st.number_input(
                        "Glucose Level", 0.0, 600.0, 90.0, format="%.1f"
                    )
                with b3:
                    hba1c = st.number_input("HbA1c (%)", 0.0, 20.0, 5.0, format="%.1f")
                with c3:
                    crp = st.number_input("CRP", 0.0, 100.0, 1.0, format="%.2f")
                with d3:
                    egfr = st.number_input("eGFR", 0.0, 200.0, 90.0, format="%.1f")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("**🧬 Data Genomik**")
                a4, b4, c4, d4 = st.columns(4)
                with a4:
                    prs_c = st.number_input(
                        "PRS Cardiometabolic", value=0.0, format="%.4f"
                    )
                with b4:
                    prs_d = st.number_input(
                        "PRS Type2Diabetes", value=0.0, format="%.4f"
                    )
                with c4:
                    apoe = st.selectbox(
                        "APOE e4 Carrier",
                        [0, 1],
                        format_func=lambda x: "Tidak" if x == 0 else "Ya",
                    )
                with d4:
                    brca = st.selectbox(
                        "BRCA Pathogenic Variant",
                        [0, 1],
                        format_func=lambda x: "Tidak" if x == 0 else "Ya",
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                bc1, bc2, bc3 = st.columns([4, 2, 2])
                with bc1:
                    submitted2 = st.form_submit_button(
                        "🔍 Prediksi Sekarang", use_container_width=True
                    )
                with bc3:
                    back_btn = st.form_submit_button(
                        "← Kembali ke Step 1", use_container_width=True
                    )

            if back_btn:
                st.session_state.step = 1
                st.rerun()

            if submitted2:
                med = {
                    "Cholesterol": chol,
                    "Glucose_Level": gluc,
                    "HbA1c": hba1c,
                    "PRS_Cardiometabolic": prs_c,
                    "PRS_Type2Diabetes": prs_d,
                    "APOE_e4_Carrier": apoe,
                    "BRCA_Pathogenic_Variant": brca,
                    "Resting_Heart_Rate": rhr,
                    "HRV": hrv,
                    "Systolic_BP": sys_bp,
                    "Diastolic_BP": dia_bp,
                    "LDL": ldl,
                    "HDL": hdl,
                    "Triglycerides": trig,
                    "CRP": crp,
                    "eGFR": egfr,
                }
                full_data = {**st.session_state.basic_data, **med}
                input_df = pd.DataFrame([full_data])[expected_columns]

                with st.spinner("Menganalisis data pasien..."):
                    pred = model.predict(input_df)
                    heart = label_mapping[pred[0][0]]
                    diabetes = label_mapping[pred[0][1]]

                    supabase.table("data_pasien").insert(
                        {
                            "age": st.session_state.basic_data["Age"],
                            "gender": st.session_state.basic_data["Gender"],
                            "bmi": st.session_state.basic_data["BMI"],
                            "smoking_status": st.session_state.basic_data[
                                "Smoking_Status"
                            ],
                            "alcohol_consumption": st.session_state.basic_data[
                                "Alcohol_Consumption"
                            ],
                            "physical_activity": st.session_state.basic_data[
                                "Physical_Activity_Level"
                            ],
                            "sleep_hours": st.session_state.basic_data["Sleep_Hours"],
                            "stress_level": st.session_state.basic_data["Stress_Level"],
                            "waist_circumference": st.session_state.basic_data[
                                "Waist_Circumference"
                            ],
                        }
                    ).execute()

                    supabase.table("hasil_prediksi").insert(
                        {"heart_risk": heart, "diabetes_risk": diabetes}
                    ).execute()

                    supabase.table("medical_data").insert(
                        {
                            "cholesterol": chol,
                            "glucose_level": gluc,
                            "hba1c": hba1c,
                            "systolic_bp": sys_bp,
                            "diastolic_bp": dia_bp,
                            "resting_heart_rate": rhr,
                            "ldl": ldl,
                            "hdl": hdl,
                            "triglycerides": trig,
                        }
                    ).execute()

                st.session_state.last_pred = (heart, diabetes, med)

            if st.session_state.last_pred:
                h_p, d_p, med = st.session_state.last_pred
                bd = st.session_state.basic_data

                st.subheader("📊 Hasil Prediksi Risiko")
                st.markdown("<div class='blue-line'></div><br>", unsafe_allow_html=True)

                show_result_panel(h_p, d_p)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='font-size:10px;font-weight:700;letter-spacing:.09em;"
                    "text-transform:uppercase;color:#60A5FA;margin:0 0 .6rem;'>📋 Ringkasan Pasien</p>",
                    unsafe_allow_html=True,
                )
                g1, g2, g3, g4, g5, g6, g7, g8 = st.columns(8)
                for col, label, val in [
                    (g1, "Umur", f"{bd['Age']} thn"),
                    (g2, "Gender", bd["Gender"]),
                    (g3, "BMI", str(bd["BMI"])),
                    (g4, "TD", f"{med['Systolic_BP']}/{med['Diastolic_BP']}"),
                    (g5, "Cholesterol", str(med["Cholesterol"])),
                    (g6, "Glucose", str(med["Glucose_Level"])),
                    (g7, "HbA1c", f"{med['HbA1c']}%"),
                    (g8, "Model", model_choice),
                ]:
                    col.markdown(
                        f"<div style='background:#F0F9FF;border:1px solid #BFDBFE;border-radius:10px;"
                        f"padding:.55rem .5rem;text-align:center;'>"
                        f"<div style='font-size:9px;color:#64748B;'>{label}</div>"
                        f"<div style='font-size:12px;font-weight:700;color:#1E293B;'>{val}</div></div>",
                        unsafe_allow_html=True,
                    )
