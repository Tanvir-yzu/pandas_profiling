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
.main-title {font-size: 2.8rem; font-weight: 700;}
.subtitle {font-size: 1.1rem; color: #6c757d; margin-bottom: 2rem;}
.card {background: rgba(255,255,255,0.04); border-radius: 14px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;}
.upload-box {border: 2px dashed #4CAF50; border-radius: 14px; padding: 30px; text-align: center; font-size: 1.1rem; color: #4CAF50;}
.info-text {font-size: 0.95rem; color: #555; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown('<div class="main-title">📊 Auto EDA Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload CSV/Excel/JSON/TXT, paste URL, or load Kaggle datasets</div>', unsafe_allow_html=True)

# ---------------- Kaggle API Setup with Environment Variables ----------------
@st.cache_resource
def get_kaggle_api(kaggle_json_content=None):
    """
    Returns authenticated KaggleApi object.
    If kaggle_json_content is provided, sets environment variables for server deployment.
    """
    if kaggle_json_content:
        token = json.loads(kaggle_json_content.decode())
        os.environ["KAGGLE_USERNAME"] = token["username"]
        os.environ["KAGGLE_KEY"] = token["key"]
    api = KaggleApi()
    api.authenticate()
    return api

# ---------------- Cached Kaggle Dataset Download ----------------
@st.cache_data(show_spinner=False, max_entries=10)
def download_kaggle_csvs(_api, dataset_name):
    """
    Downloads Kaggle dataset CSVs to a temp folder.
    Returns dict {filename: full_path}.
    _api: prefixed with _ to avoid Streamlit hashing issues.
    """
    temp_dir = tempfile.mkdtemp()
    _api.dataset_download_files(dataset_name, path=temp_dir, unzip=True)
    csv_files = [f for f in os.listdir(temp_dir) if f.endswith(".csv")]
    if not csv_files:
        raise Exception("No CSV file found in Kaggle dataset")
    return {f: os.path.join(temp_dir, f) for f in csv_files}

# ---------------- Input Section ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(
    ["📁 Upload File", "🌐 CSV URL", "🏆 Kaggle Dataset", "🔐 Kaggle Token"]
)

df = None

# ---- File Upload ----
with tab1:
    st.markdown('<div class="upload-box">⬇️ Drag & Drop your file here</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Supported formats: CSV (.csv), Excel (.xlsx, .xls), JSON (.json), TXT (.txt)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload your file",
        type=["csv", "xlsx", "xls", "json", "txt"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv") or uploaded_file.name.endswith(".txt"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)
        except Exception as e:
            st.error(f"❌ Could not read file: {e}")

# ---- CSV URL ----
with tab2:
    st.markdown('<div class="info-text">Enter a direct CSV URL. Supported format: CSV (.csv)</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="info-text">Enter Kaggle dataset in the format <owner/dataset-name>. Example: heptapod/titanic</div>', unsafe_allow_html=True)
    kaggle_dataset_name = st.text_input(
        "Enter Kaggle dataset name (owner/dataset-name)",
        placeholder="heptapod/titanic"
    )
    selected_csv = None
    kaggle_file_uploaded = None

    # Upload Kaggle API token first (server-safe)
    kaggle_file_uploaded = st.file_uploader(
        "Upload kaggle.json token for server deployment",
        type=["json"],
        label_visibility="collapsed"
    )

    if kaggle_dataset_name and kaggle_file_uploaded:
        try:
            api = get_kaggle_api(kaggle_file_uploaded.read())
            kaggle_csv_files = download_kaggle_csvs(api, kaggle_dataset_name)
            selected_csv = st.selectbox("Select CSV to analyze", list(kaggle_csv_files.keys()))
            if selected_csv:
                df = pd.read_csv(kaggle_csv_files[selected_csv])
        except Exception as e:
            st.error(f"Kaggle download failed: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Data Preview & EDA ----------------
if df is not None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.success("✅ Dataset Loaded Successfully")
    st.markdown("#### 👀 Preview")
    st.dataframe(df.head(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generate = st.button("🚀 Generate EDA Report", use_container_width=True)

    if generate:
        with st.spinner("🔍 Generating EDA report..."):
            profile = ProfileReport(df, title="Auto EDA Report", explorative=True)
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
st.caption("⚡ Built with Streamlit • ydata-profiling • Kaggle API • Server-ready & Cached")
