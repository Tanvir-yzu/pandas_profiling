import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from io import StringIO
import requests
import tempfile

# ---------- Page Config ----------
st.set_page_config(
    page_title="Auto EDA Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 14px;
        padding: 35px;
        text-align: center;
        font-size: 1.1rem;
        color: #4CAF50;
        margin-bottom: 15px;
    }
    .divider {
        text-align: center;
        margin: 20px 0;
        font-weight: 600;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="main-title">📊 Auto EDA Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a dataset or paste a CSV URL and instantly get a professional EDA report</div>', unsafe_allow_html=True)

# ---------- Input Card ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="upload-box">⬇️ Drag & Drop your CSV file here</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv"])

st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
csv_url = st.text_input("🌐 Paste CSV URL")

st.markdown('</div>', unsafe_allow_html=True)

df = None

# ---------- Load Data ----------
if uploaded_file:
    df = pd.read_csv(uploaded_file)

elif csv_url:
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
    except:
        st.error("❌ Failed to load CSV from URL")

# ---------- Data Preview ----------
if df is not None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.success("✅ Dataset Loaded Successfully")
    st.markdown("#### 👀 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Generate Button ----------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate = st.button("🚀 Generate EDA Report", use_container_width=True)

    if generate:
        with st.spinner("🔍 Analyzing data & generating report..."):
            profile = ProfileReport(
                df,
                title="Auto EDA Report",
                explorative=True
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
                profile.to_file(tmp.name)
                html_path = tmp.name

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## 📈 EDA Report")

        with open(html_path, "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=1000, scrolling=True)

        with open(html_path, "rb") as f:
            st.download_button(
                "⬇️ Download HTML Report",
                f,
                file_name="eda_report.html",
                mime="text/html"
            )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("⚡ Built with Streamlit & ydata-profiling")
