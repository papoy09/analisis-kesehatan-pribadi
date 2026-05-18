import streamlit as st

# ==========================
# STYLE
# ==========================


def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root{
            --primary:#60A5FA; --secondary:#7DD3FC; --accent:#BAE6FD;
            --success:#22C55E; --warning:#F59E0B; --danger:#EF4444;
            --dark:#E0F2FE; --card:#FFFFFF;
        }

        html, body, [class*="css"]{
            font-family:'Inter',sans-serif !important;
            background:
                radial-gradient(circle at top left,#EFF6FF 0%,transparent 30%),
                radial-gradient(circle at bottom right,#DBEAFE 0%,transparent 35%),
                linear-gradient(180deg,#F8FCFF 0%,#EEF8FF 100%);
            color:#0F172A;
        }

        #MainMenu, footer, header{ visibility:hidden; }
        .block-container{ padding-top:1.2rem; max-width:1250px; }

        .main::before{
            content:''; position:fixed; width:500px; height:500px;
            background:rgba(147,197,253,.25); filter:blur(120px);
            top:-120px; right:-100px; z-index:-1;
        }
        .main::after{
            content:''; position:fixed; width:450px; height:450px;
            background:rgba(191,219,254,.25); filter:blur(120px);
            bottom:-120px; left:-100px; z-index:-1;
        }

        [data-testid="stSidebar"]{
            background:linear-gradient(180deg,#BFDBFE 0%,#93C5FD 45%,#60A5FA 100%) !important;
            border-right:1px solid rgba(255,255,255,.25);
        }
        [data-testid="stSidebar"] > div:first-child{ padding-top:2rem; }
        [data-testid="stSidebar"] label{ color:white !important; font-size:12px !important; font-weight:600 !important; }
        [data-testid="stSidebar"] span{ color:#EFF6FF !important; }

        .glass-card{
            background:rgba(255,255,255,.92); backdrop-filter:blur(18px);
            border:1px solid rgba(255,255,255,.85); border-radius:22px; padding:1.5rem;
            box-shadow:0 10px 40px rgba(96,165,250,.12),inset 0 1px 0 rgba(255,255,255,.8);
            transition:all .3s ease; margin-bottom:1rem;
        }
        .glass-card:hover{ transform:translateY(-2px); }

        .metric-card{
            background:linear-gradient(145deg,#FFFFFF,#F0F9FF); border-radius:22px;
            padding:1.2rem; border:1px solid #DBEAFE; text-align:center;
            box-shadow:0 10px 25px rgba(96,165,250,.10); transition:all .3s ease;
            position:relative; overflow:hidden;
        }
        .metric-card::before{
            content:''; position:absolute; width:120px; height:120px;
            background:rgba(125,211,252,.18); border-radius:50%; top:-50px; right:-40px;
        }
        .metric-card:hover{ transform:translateY(-4px); box-shadow:0 18px 35px rgba(96,165,250,.18); }
        .metric-title{ font-size:12px; color:#64748B; margin-bottom:8px; }
        .metric-value{ font-size:28px; font-weight:800; color:#1E3A8A; }

        .stButton > button{
            width:100%;
            background:linear-gradient(135deg,#93C5FD 0%,#60A5FA 50%,#38BDF8 100%) !important;
            color:white !important; border:none !important; border-radius:14px !important;
            padding:.8rem 1.4rem !important; font-weight:700 !important; font-size:14px !important;
            box-shadow:0 10px 25px rgba(96,165,250,.22); transition:all .25s ease !important;
        }
        .stButton > button:hover{ transform:translateY(-2px) scale(1.01); box-shadow:0 15px 35px rgba(96,165,250,.28); }

        input, textarea{ border-radius:12px !important; }
        .stSelectbox > div > div{ border-radius:12px !important; border:1px solid #BFDBFE !important; background:#FFFFFF !important; }
        .stNumberInput > div > div > input{ border-radius:12px !important; }

        .stDownloadButton > button{
            width:100%; border-radius:14px !important; border:none !important;
            background:linear-gradient(135deg,#7DD3FC,#38BDF8) !important;
            color:white !important; font-weight:700 !important; padding:.8rem !important;
        }

        .badge-success{ background:#DCFCE7; color:#166534; padding:.25rem .7rem; border-radius:999px; font-size:10px; font-weight:700; }
        .badge-warning{ background:#FEF3C7; color:#92400E; padding:.25rem .7rem; border-radius:999px; font-size:10px; font-weight:700; }
        .badge-danger{  background:#FEE2E2; color:#991B1B; padding:.25rem .7rem; border-radius:999px; font-size:10px; font-weight:700; }

        ::-webkit-scrollbar{ width:8px; }
        ::-webkit-scrollbar-thumb{ background:linear-gradient(#BAE6FD,#60A5FA); border-radius:999px; }

        [data-testid="stDataFrame"]{ border-radius:18px !important; overflow:hidden !important; border:1px solid #DBEAFE !important; }
        .stSuccess{ border-radius:16px !important; background:#ECFEFF !important; border:1px solid #BAE6FD !important; }

        .info-box{
            background:linear-gradient(135deg,#E0F2FE,#F0F9FF); border:1px solid #BAE6FD;
            padding:1rem; border-radius:18px; margin-top:1rem; color:#0F172A;
        }

        .soft-card{
            background:#FFFFFF; border:1px solid #E0F2FE; border-radius:20px;
            padding:1rem; box-shadow:0 6px 18px rgba(96,165,250,.08);
        }
        .blue-line{ height:5px; border-radius:999px; background:linear-gradient(90deg,#7DD3FC,#60A5FA,#38BDF8); margin-top:.7rem; }
        .status-pill{ display:inline-block; padding:.35rem .8rem; border-radius:999px; background:#DBEAFE; color:#1D4ED8; font-size:11px; font-weight:700; }

        .small-card{
            background:#F8FCFF; border:1px solid #DBEAFE; border-radius:18px;
            padding:1rem; text-align:center; transition:all .25s ease;
        }
        .small-card:hover{ transform:translateY(-2px); }
        .small-number{ font-size:24px; font-weight:800; color:#2563EB; }
        .small-text{ font-size:12px; color:#64748B; }

        .step-bar{
            display:flex; gap:0; margin-bottom:1.2rem;
            border:1px solid #DBEAFE; border-radius:14px; overflow:hidden;
        }
        .step-active{
            flex:1; padding:.6rem 1rem; background:#60A5FA;
            color:white; font-size:13px; font-weight:700; text-align:center;
        }
        .step-done{
            flex:1; padding:.6rem 1rem; background:#DBEAFE;
            color:#1E40AF; font-size:13px; font-weight:600; text-align:center;
        }
        .step-inactive{
            flex:1; padding:.6rem 1rem; background:#F8FCFF;
            color:#94A3B8; font-size:13px; font-weight:500; text-align:center;
            border-left:1px solid #DBEAFE;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
