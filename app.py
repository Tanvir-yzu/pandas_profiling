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

# ---------------- Sidebar Navigation ----------------
page = st.sidebar.radio(
    "📌 Navigation",
    ["📊 Auto EDA App", "📘 Kaggle Token Doc"]
)


# ---------------- Custom CSS for Black BG & Colorful UI ----------------
st.markdown("""
<style>
/* Full page black background */
[data-testid="stAppViewContainer"] {
    background-color: #004C32;
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

# ====================================================
# 📘 API DOCUMENTATION PAGE
# ====================================================
if page == "📘 Kaggle Token Doc":

    st.markdown('<div class="main-title">📘 Kaggle Token Documentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Auto EDA Generator – Usage Guide & Integration</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    🚀 Overview

    The **Auto EDA Generator** automatically creates an **Exploratory Data Analysis (EDA) HTML report** from structured datasets with no manual coding required.

    ---

    * **Kaggle Datasets**

    * Load datasets directly from Kaggle using the Kaggle API
    * Requires a `kaggle.json` authentication file

    ---

    ## 🔐 Kaggle API Setup

    To access Kaggle datasets, you must create and upload a **Kaggle API token**.

    ### Step 1: Generate Kaggle API Token

    Visit the following link and create a new API token:

    ```
    https://www.kaggle.com/settings
    ```

    Download the file named **`kaggle.json`**.

    ---

    ### Step 2: kaggle.json File Format

    Your `kaggle.json` file should contain the following:

    ```json
    {
    "username": "your_kaggle_username",
    "key": "your_kaggle_api_key"
    }
    ```

    ---

    ### Step 3: Upload in Application

    * Upload `kaggle.json` once in the **Kaggle Token** section
    * The token is stored securely for future use
    * If the token already exists, the app will notify you that it is up to date
    ---

    ## 📂 Supported File Formats
    | Format | Extension |
    |------|-----------|
    | CSV | `.csv` |
    | Excel | `.xlsx`, `.xls` |
    | JSON | `.json` |
    | Text | `.txt` |

    ---

    ## 🏆 Kaggle Dataset Usage
    **Dataset format:**
    ```
    owner/dataset-name
    ```
    **Example:**
    ```
    heptapod/titanic
    ```

    **Steps:**
    1. Upload `kaggle.json` once
    2. It is stored securely in local storage
    3. Select dataset CSV
    4. Generate EDA

    ---

    ## 📄 Output
    - Interactive HTML EDA Report
    - Downloadable `.html` file
    - Filename matches input dataset name

    ---

    ## 🔐 Security
    - `kaggle.json` stored in `~/.kaggle/`
    - File permissions set to `600`
    - Cached securely using Streamlit

    ---

    ## 📞 Contact
    **Developer:** Tanvir  
    **Email:** 2020tanvir1971@gmail.com  
    **Phone:** +88 0173837737  

    </div>
    """, unsafe_allow_html=True)

# ====================================================
# 📊 MAIN AUTO EDA APP PAGE
# ====================================================
else:

        # ---------------- Header ----------------
        st.markdown('<div class="main-title">📊 Auto EDA Generator</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Upload CSV/Excel/JSON/TXT, paste URL, or load Kaggle datasets</div>', unsafe_allow_html=True)

        # ---------------- Safe file loader ----------------
        def load_file(file):
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
            try:
                return pd.read_csv(string_io)
            except Exception as e:
                st.error(f"❌ Could not read CSV ({name}): {e}")
                return None

        # ---------------- Kaggle API Setup with Local Storage ----------------
        @st.cache_resource
        def get_kaggle_api(kaggle_json_content=None):
            kaggle_path = Path.home() / ".kaggle"
            kaggle_path.mkdir(exist_ok=True)
            
            if kaggle_json_content:
                kaggle_file = kaggle_path / "kaggle.json"
                with open(kaggle_file, "wb") as f:
                    f.write(kaggle_json_content)
                os.chmod(kaggle_file, 0o600)
                st.success("✅ kaggle.json saved locally")

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
        # ---- CSV URL ----
            with tab2:
                st.markdown(
                    '<div class="info-text">'
                    'Paste a CSV URL, GitHub file link, or Google Drive share link. '
                    'Links are auto-converted.'
                    '</div>',
                    unsafe_allow_html=True
                )

                csv_url = st.text_input(
                    "Paste CSV / GitHub / Google Drive URL",
                    placeholder="GitHub or Google Drive CSV link"
                )

                if csv_url:
                    try:
                        original_url = csv_url.strip()

                        # ✅ GitHub blob → raw
                        if "github.com" in original_url and "/blob/" in original_url:
                            csv_url = original_url.replace(
                                "https://github.com/",
                                "https://raw.githubusercontent.com/"
                            ).replace("/blob/", "/")

                            st.info(f"🔁 GitHub link converted:\n{csv_url}")

                        # ✅ Google Drive → direct download
                        elif "drive.google.com" in original_url:
                            import re
                            match = re.search(r"/d/([a-zA-Z0-9_-]+)", original_url)
                            if match:
                                file_id = match.group(1)
                                csv_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                                st.info(f"🔁 Google Drive link converted:\n{csv_url}")
                            else:
                                st.error("❌ Invalid Google Drive link format")
                                csv_url = None

                        if csv_url:
                            input_name = Path(csv_url).stem
                            response = requests.get(csv_url, timeout=20)
                            response.raise_for_status()

                            # 🚫 HTML protection
                            if "<html" in response.text.lower():
                                st.error(
                                    "❌ The link does not provide raw CSV data.\n\n"
                                    "Make sure the file is shared publicly and is a CSV."
                                )
                            else:
                                df = load_csv_stringio(StringIO(response.text), csv_url)
                                if df is not None:
                                    st.success("✅ CSV loaded successfully")

                    except Exception as e:
                        st.error(f"❌ Failed to load CSV: {e}")



        # ---- Kaggle Dataset ----
            with tab3:
                st.markdown(
                    '<div class="info-text">'
                    'Enter Kaggle dataset in the format <owner/dataset-name>. '
                    'Supports datasets with multiple CSV files.'
                    '</div>',
                    unsafe_allow_html=True
                )

                kaggle_dataset_name = st.text_input(
                    "Enter Kaggle dataset name (owner/dataset-name)",
                    placeholder="heptapod/titanic"
                )

                if kaggle_dataset_name:
                    try:
                        api = get_kaggle_api()  # uses locally saved kaggle.json
                        kaggle_csv_files = download_kaggle_csvs(api, kaggle_dataset_name)

                        csv_names = list(kaggle_csv_files.keys())

                        st.success(f"✅ Found {len(csv_names)} CSV file(s)")

                        # ---------- Handling mode ----------
                        mode = st.radio(
                            "How would you like to handle the CSV files?",
                            [
                                "📄 Analyze a single CSV",
                                "🧩 Merge all CSVs (row-wise)",
                                "📊 Generate EDA for each CSV separately"
                            ]
                        )

                        # ---------- Option 1: Single CSV ----------
                        if mode == "📄 Analyze a single CSV":
                            selected_csv = st.selectbox("Select CSV to analyze", csv_names)
                            if selected_csv:
                                df = load_file(open(kaggle_csv_files[selected_csv], "rb"))
                                input_name = Path(selected_csv).stem

                        # ---------- Option 2: Merge all CSVs ----------
                        elif mode == "🧩 Merge all CSVs (row-wise)":
                            dfs = []
                            for csv_file in csv_names:
                                temp_df = load_file(open(kaggle_csv_files[csv_file], "rb"))
                                if temp_df is not None:
                                    temp_df["__source_file__"] = csv_file
                                    dfs.append(temp_df)

                            if dfs:
                                df = pd.concat(dfs, ignore_index=True)
                                input_name = kaggle_dataset_name.replace("/", "_") + "_merged"
                                st.success("✅ All CSV files merged successfully")

                        # ---------- Option 3: Multi-EDA ----------
                        elif mode == "📊 Generate EDA for each CSV separately":
                            selected_csvs = st.multiselect(
                                "Select one or more CSV files",
                                csv_names,
                                default=csv_names
                            )

                            if selected_csvs:
                                st.info("ℹ️ EDA reports will be generated one by one")

                                for csv_file in selected_csvs:
                                    temp_df = load_file(open(kaggle_csv_files[csv_file], "rb"))
                                    if temp_df is not None:
                                        st.markdown(f"### 📈 EDA for `{csv_file}`")
                                        profile = ProfileReport(
                                            temp_df,
                                            title=f"{csv_file} EDA Report",
                                            explorative=True
                                        )
                                        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
                                            profile.to_file(tmp.name)

                                        with open(tmp.name, "r", encoding="utf-8") as f:
                                            st.components.v1.html(f.read(), height=600, scrolling=True)

                                        with open(tmp.name, "rb") as f:
                                            st.download_button(
                                                f"⬇️ Download {csv_file} EDA",
                                                f,
                                                file_name=f"{Path(csv_file).stem}_eda.html",
                                                mime="text/html"
                                            )

                    except Exception as e:
                        st.error(f"Kaggle download failed: {e}")


        # ---- Kaggle Token Upload ----
        with tab4:
            st.markdown('<div class="info-text">Upload your kaggle.json (only once, it will be saved locally)</div>', unsafe_allow_html=True)
            kaggle_file_uploaded = st.file_uploader(
                "Upload kaggle.json token",
                type=["json"],
                label_visibility="collapsed"
            )
            if kaggle_file_uploaded:
                try:
                    get_kaggle_api(kaggle_file_uploaded.read())
                except Exception as e:
                    st.error(f"Kaggle API setup failed: {e}")

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

                st.markdown('<div class="eda-card">', unsafe_allow_html=True)
                st.markdown(f"## 📈 {input_name} EDA Report Preview")
                with open(html_path, "r", encoding="utf-8") as f:
                    st.components.v1.html(f.read(), height=1000, scrolling=True)

                with open(html_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download HTML Report",
                        f,
                        file_name=report_name,
                        mime="text/html"
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- Footer with Contact Info ----------------
        st.markdown("""
        <hr style="border:1px solid #444444">
        <div style="text-align:center; color:#ffffff; font-size:0.9rem; margin-top:10px;">
        ⚡ Built with Streamlit • ydata-profiling • Kaggle API • Black Background & Gradient UI • Safe File Loader <br>
        📧 Contact: 2020tanvir1971@gmail.com | 🌐 Website: https://yourwebsite.com | 📱 Phone: +88 0173837737
        </div>
        """, unsafe_allow_html=True)
