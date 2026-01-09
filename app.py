import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from io import StringIO
import requests
import tempfile
import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Auto EDA Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Custom CSS for Black BG & Colorful UI ----------------
st.markdown("""
<style>
/* Full page black background */
[data-testid="stAppViewContainer"] {
    background-color: #0B544C;
    color: #ffffff;
}

/* Header titles */
.main-title {font-size: 3rem; font-weight: 700; color: #ffffff; text-shadow: 2px 2px 5px #FF5733;}
.subtitle {font-size: 1.2rem; color: #dddddd; margin-bottom: 2rem;}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 8px 20px rgba(255,255,255,0.15);
    margin-bottom: 25px;
}

/* Drag & Drop box */
.upload-box {
    border: 2px dashed #FFD700;
    border-radius: 14px;
    padding: 40px;
    text-align: center;
    font-size: 1.2rem;
    color: #FFD700;
    font-weight: 600;
    transition: 0.3s;
}
.upload-box:hover {
    background: rgba(255, 255, 255, 0.1);
}

/* Info text */
.info-text {font-size: 0.95rem; color: #f0f0f0; margin-bottom: 10px;}

/* EDA Report card */
.eda-card {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    color: #ffffff;
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(255, 75, 43, 0.5);
}

/* Download button */
.st-download-button>button {
    background: linear-gradient(135deg, #36D1DC, #5B86E5);
    color: white;
    font-weight: 700;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s;
}
.st-download-button>button:hover {
    background: linear-gradient(135deg, #5B86E5, #36D1DC);
    transform: translateY(-2px);
}

/* Footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown('<div class="main-title">📊 Auto EDA Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload CSV/Excel/JSON/TXT, paste URL, or load Kaggle datasets</div>', unsafe_allow_html=True)

# ---------------- Safe file loader ----------------
def load_file(file):
    """Load CSV, Excel, JSON, TXT safely with friendly error messages"""
    try:
        if file.name.endswith(".csv") or file.name.endswith(".txt"):
            return pd.read_csv(file)
        elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
            try:
                import openpyxl
                return pd.read_excel(file)
            except ModuleNotFoundError:
                st.error("❌ Excel files require 'openpyxl'. Install it using `pip install openpyxl`")
                return None
        elif file.name.endswith(".json"):
            return pd.read_json(file)
    except Exception as e:
        st.error(f"❌ Could not read file: {e}")
        return None

def load_csv_stringio(string_io, name="dataset"):
    """Load CSV from StringIO safely"""
    try:
        return pd.read_csv(string_io)
    except Exception as e:
        st.error(f"❌ Could not read CSV ({name}): {e}")
        return None

# ---------------- Kaggle API Setup ----------------
@st.cache_resource
def get_kaggle_api(kaggle_json_content=None):
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
input_name = "dataset"

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
        input_name = Path(uploaded_file.name).stem
        df = load_file(uploaded_file)

# ---- CSV URL ----
with tab2:
    st.markdown('<div class="info-text">Enter a direct CSV URL. Supported format: CSV (.csv)</div>', unsafe_allow_html=True)
    csv_url = st.text_input("Paste direct CSV URL")
    if csv_url:
        input_name = Path(csv_url).stem
        try:
            response = requests.get(csv_url)
            response.raise_for_status()
            df = load_csv_stringio(StringIO(response.text), csv_url)
        except Exception as e:
            st.error(f"❌ Failed to load CSV from URL: {e}")

# ---- Kaggle Dataset ----
with tab3:
    st.markdown('<div class="info-text">Enter Kaggle dataset in the format <owner/dataset-name></div>', unsafe_allow_html=True)
    kaggle_dataset_name = st.text_input(
        "Enter Kaggle dataset name (owner/dataset-name)",
        placeholder="heptapod/titanic"
    )
    selected_csv = None
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
                df = load_file(open(kaggle_csv_files[selected_csv], "rb"))
                input_name = Path(selected_csv).stem
        except Exception as e:
            st.error(f"Kaggle download failed: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Data Preview & EDA ----------------
if df is not None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.success("✅ Dataset Loaded Successfully")
    st.markdown(f"#### 👀 {input_name} Preview")
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generate = st.button("🚀 Generate EDA Report", use_container_width=True)

    if generate:
        with st.spinner("🔍 Generating EDA report..."):
            profile = ProfileReport(df, title=f"{input_name} EDA Report", explorative=True)
            report_name = f"{input_name}_eda.html"
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
                profile.to_file(tmp.name)
                html_path = tmp.name

        # Gradient themed EDA card
        st.markdown('<div class="eda-card">', unsafe_allow_html=True)
        st.markdown(f"## 📈 {input_name} EDA Report Preview")
        with open(html_path, "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=1000, scrolling=True)

        # Download button with gradient theme
        with open(html_path, "rb") as f:
            st.download_button(
                "⬇️ Download HTML Report",
                f,
                file_name=report_name,
                mime="text/html"
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown("---")
st.caption("⚡ Built with Streamlit • ydata-profiling • Kaggle API • Black Background & Gradient UI • Safe File Loader")
