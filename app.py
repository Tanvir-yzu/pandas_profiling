import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from io import StringIO
import requests
import tempfile
import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Auto EDA Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
.main-title {
    font-size: 2.8rem;
    font-weight: 700;
}
.subtitle {
    font-size: 1.1rem;
    color: #6c757d;
    margin-bottom: 2rem;
}
.card {
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.upload-box {
    border: 2px dashed #4CAF50;
    border-radius: 14px;
    padding: 30px;
    text-align: center;
    font-size: 1.1rem;
    color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown('<div class="main-title">📊 Auto EDA Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Upload CSV, use URL, or load Kaggle datasets using kaggle.json</div>',
    unsafe_allow_html=True
)

# ---------------- Kaggle Auth via UI ----------------
def setup_kaggle_from_upload(uploaded_kaggle_file):
    kaggle_dir = os.path.join(os.path.expanduser("~"), ".kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)

    kaggle_path = os.path.join(kaggle_dir, "kaggle.json")

    with open(kaggle_path, "wb") as f:
        f.write(uploaded_kaggle_file.read())

    # Set permissions (important for Kaggle)
    try:
        os.chmod(kaggle_path, 0o600)
    except:
        pass

    return True

# ---------------- Kaggle Loader ----------------
def load_kaggle_dataset(dataset_name):
    api = KaggleApi()
    api.authenticate()

    temp_dir = tempfile.mkdtemp()
    api.dataset_download_files(
        dataset_name,
        path=temp_dir,
        unzip=True
    )

    csv_files = [f for f in os.listdir(temp_dir) if f.endswith(".csv")]

    if not csv_files:
        raise Exception("No CSV file found in Kaggle dataset")

    return pd.read_csv(os.path.join(temp_dir, csv_files[0]))

# ---------------- Input Section ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📁 Upload CSV", "🌐 CSV URL", "🏆 Kaggle Dataset", "🔐 Kaggle Token"]
)

df = None

# ---- Upload CSV ----
with tab1:
    st.markdown('<div class="upload-box">⬇️ Drag & Drop CSV file here</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

# ---- CSV URL ----
with tab2:
    csv_url = st.text_input("Paste direct CSV URL")
    if csv_url:
        try:
            response = requests.get(csv_url)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))
        except:
            st.error("❌ Failed to load CSV from URL")

# ---- Kaggle Dataset ----
with tab3:
    kaggle_dataset = st.text_input(
        "Enter Kaggle dataset name (owner/dataset-name)",
        placeholder="heptapod/titanic"
    )
    if kaggle_dataset:
        try:
            df = load_kaggle_dataset(kaggle_dataset)
        except Exception as e:
            st.error(f"❌ {e}")

# ---- Kaggle Token Upload ----
with tab4:
    st.markdown("### Upload kaggle.json")
    kaggle_file = st.file_uploader(
        "Upload your kaggle.json file",
        type=["json"]
    )

    if kaggle_file:
        try:
            setup_kaggle_from_upload(kaggle_file)
            st.success("✅ Kaggle API token configured successfully!")
        except:
            st.error("❌ Invalid kaggle.json file")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Data Preview & EDA ----------------
if df is not None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.success("✅ Dataset Loaded Successfully")
    st.markdown("#### 👀 Preview")
    st.dataframe(df.head(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate = st.button("🚀 Generate EDA Report", use_container_width=True)

    if generate:
        with st.spinner("🔍 Generating EDA report..."):
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

# ---------------- Footer ----------------
st.markdown("---")
st.caption("⚡ Built with Streamlit • ydata-profiling • Kaggle API")
