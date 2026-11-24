import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from io import StringIO, BytesIO
from urllib.parse import urlparse
import requests
import tempfile
import os
import re
import csv
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI/ML DataSets EDA Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Custom CSS (modern, version-safe selectors) ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

@keyframes gradientFlow {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
@keyframes fadeInUp {
    from {opacity: 0; transform: translateY(14px);}
    to {opacity: 1; transform: translateY(0);}
}
@keyframes pulseDot {
    0% {box-shadow: 0 0 0 0 rgba(46, 213, 115, 0.55);}
    70% {box-shadow: 0 0 0 8px rgba(46, 213, 115, 0);}
    100% {box-shadow: 0 0 0 0 rgba(46, 213, 115, 0);}
}

.main-title {
    font-size: 2.7rem;
    font-weight: 800;
    background: linear-gradient(90deg, #7C6CF5, #00D9C0, #7C6CF5);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
    animation: gradientFlow 6s ease-in-out infinite;
}
.subtitle {
    font-size: 1.05rem;
    color: #a9adc1;
    margin-bottom: 1.2rem;
    animation: fadeInUp 0.5s ease both;
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 1.6rem;
    animation: fadeInUp 0.5s ease 0.1s both;
}
.badge {
    display: inline-block;
    background: rgba(124, 108, 245, 0.12);
    border: 1px solid rgba(124, 108, 245, 0.35);
    color: #cfc9ff;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 999px;
    transition: transform 0.15s ease, background 0.15s ease;
}
.badge:hover {
    transform: translateY(-2px) scale(1.05);
    background: rgba(124, 108, 245, 0.22);
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #2ed573;
    margin-right: 6px;
    animation: pulseDot 2s infinite;
}

.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 22px;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.card:hover {border-color: rgba(124, 108, 245, 0.35);}

.info-text {font-size: 0.92rem; color: #a9adc1; margin-bottom: 10px;}

.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f2f3f7;
    margin: 0 0 16px 0;
}

.feature-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 20px;
    height: 100%;
    animation: fadeInUp 0.5s ease both;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.feature-card:hover {
    transform: translateY(-3px);
    border-color: rgba(124, 108, 245, 0.35);
}
.feature-card .icon {font-size: 1.6rem; margin-bottom: 8px;}
.feature-card .title {font-weight: 700; color: #f2f3f7; margin-bottom: 4px;}
.feature-card .desc {font-size: 0.85rem; color: #a9adc1; line-height: 1.4;}

.eda-card {
    background: linear-gradient(135deg, #7C6CF5, #00D9C0);
    color: #0F1117;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 20px;
    animation: fadeInUp 0.4s ease both;
}
.eda-card h2 {color: #0F1117;}

@media (prefers-reduced-motion: reduce) {
    * {animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; transition-duration: 0.001ms !important;}
}

/* Buttons */
.stButton>button, .stDownloadButton>button {
    border-radius: 10px;
    font-weight: 700;
    border: none;
    padding: 0.6rem 1.2rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(124, 108, 245, 0.35);
}
.stButton>button[kind="primary"] {
    background: linear-gradient(90deg, #7C6CF5, #6A5AE0);
}

/* Tabs — pill style */
[data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
[data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    padding: 8px 18px;
    font-weight: 600;
    color: #a9adc1;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: #ffffff !important;
    background: rgba(124, 108, 245, 0.15);
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 14px 18px;
}

hr {border-color: rgba(255,255,255,0.08) !important;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar Navigation ----------------
with st.sidebar:
    st.markdown(
        '<div style="font-size:1.6rem; font-weight:800;">📊 EDA Studio</div>'
        '<div style="color:#a9adc1; font-size:0.85rem; margin-bottom:1.2rem;">'
        'AI/ML DataSets EDA Generator</div>',
        unsafe_allow_html=True
    )
    page = st.radio(
        "📌 Navigation",
        ["📊 AI/ML DataSets EDA", "📘 Kaggle Token Doc"],
        label_visibility="collapsed"
    )
    st.divider()
    kaggle_token_path = Path.home() / ".kaggle" / "kaggle.json"
    if kaggle_token_path.exists():
        st.markdown(
            '<span class="status-dot"></span>'
            '<span style="font-size:0.85rem; color:#a9adc1;">Kaggle token configured</span>',
            unsafe_allow_html=True
        )
    else:
        st.caption("⚪ Kaggle token not set")
    st.caption("Built with Streamlit • ydata-profiling")


# ---------------- Shared Helpers ----------------
def sanitize_filename(name, fallback="dataset"):
    name = urlparse(name).path if "://" in name else name
    name = Path(name).stem
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" ._")
    return name or fallback


def decode_bytes(data):
    """Decode raw bytes, falling back through common encodings."""
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1")  # never fails


def read_csv_robust(text, name="dataset"):
    """
    Parse delimited text, tolerating messy files:
      1. detect the delimiter (, ; tab |) from a sample of lines
      2. fast C parser with that delimiter
      3. skip malformed rows (wrong number of fields) and warn the user
    """
    sep = ","
    try:
        sample = "\n".join(text.splitlines()[:50])
        sep = csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        pass

    try:
        return pd.read_csv(StringIO(text), sep=sep)
    except pd.errors.ParserError:
        pass

    bad_lines = []

    def _skip(line):
        bad_lines.append(line)
        return None  # drop the row

    df = pd.read_csv(StringIO(text), sep=sep, engine="python", on_bad_lines=_skip)
    if bad_lines:
        st.warning(
            f"⚠️ {name}: skipped {len(bad_lines)} malformed row(s) whose field count "
            f"did not match the header ({len(df.columns)} columns). "
            "This is usually caused by unquoted delimiters inside values."
        )
    return df


def load_file(file):
    name = Path(file.name).name
    lower = name.lower()
    try:
        if lower.endswith((".csv", ".txt", ".tsv")):
            raw = file.read()
            text = decode_bytes(raw) if isinstance(raw, bytes) else raw
            return read_csv_robust(text, name)
        elif lower.endswith((".xlsx", ".xls")):
            try:
                return pd.read_excel(file)
            except ImportError as e:
                engine = "xlrd" if lower.endswith(".xls") else "openpyxl"
                st.error(f"❌ Excel support requires '{engine}'. Install it using `pip install {engine}` ({e})")
                return None
        elif lower.endswith(".json"):
            return pd.read_json(file)
        else:
            st.error(f"❌ Unsupported file type: {name}")
            return None
    except Exception as e:
        st.error(f"❌ Could not read file ({name}): {e}")
        return None


def load_path(path):
    with open(path, "rb") as f:
        return load_file(f)


def load_csv_stringio(string_io, name="dataset"):
    try:
        return read_csv_robust(string_io.getvalue(), name)
    except Exception as e:
        st.error(f"❌ Could not read CSV ({name}): {e}")
        return None


def render_profile_report(dataframe, title, download_label, file_name, height=600):
    try:
        profile = ProfileReport(dataframe, title=title, explorative=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            tmp_path = tmp.name
        try:
            profile.to_file(tmp_path)
            with open(tmp_path, "r", encoding="utf-8") as f:
                html = f.read()
        finally:
            os.remove(tmp_path)

        st.components.v1.html(html, height=height, scrolling=True)
        st.download_button(
            download_label,
            html.encode("utf-8"),
            file_name=file_name,
            mime="text/html"
        )
    except Exception as e:
        st.error(f"Failed to generate EDA report: {e}")


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


@st.cache_data(show_spinner=False, max_entries=10)
def download_kaggle_csvs(_api, dataset_name):
    temp_dir = tempfile.mkdtemp()
    _api.dataset_download_files(dataset_name, path=temp_dir, unzip=True)
    csv_files = [f for f in os.listdir(temp_dir) if f.endswith(".csv")]
    if not csv_files:
        raise Exception("No CSV file found in Kaggle dataset")
    return {f: os.path.join(temp_dir, f) for f in csv_files}


# ====================================================
# 📘 API DOCUMENTATION PAGE
# ====================================================
if page == "📘 Kaggle Token Doc":

    st.markdown('<div class="main-title">📘 Kaggle Token Documentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI/ML DataSets EDA Generator – Usage Guide & Integration</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="card">

## 🚀 Overview

The **AI/ML DataSets EDA Generator** automatically creates an **Exploratory Data Analysis (EDA) HTML report** from structured datasets with no manual coding required.

* **Kaggle Datasets** — load datasets directly via the Kaggle API. Requires a `kaggle.json` authentication file.

---

## 🔐 Kaggle API Setup

**Step 1 — Generate a token:** visit `https://www.kaggle.com/settings` and create a new API token, which downloads `kaggle.json`.

**Step 2 — File format:**
```json
{
  "username": "your_kaggle_username",
  "key": "your_kaggle_api_key"
}
```

**Step 3 — Upload it once** in the **Kaggle Token** tab. It's stored securely for future use; if it already exists, the app will tell you it's configured.

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
**Format:** `owner/dataset-name` — **Example:** `heptapod/titanic`

1. Upload `kaggle.json` once
2. It is stored securely on disk
3. Select a dataset CSV
4. Generate the EDA report

---

## 🔐 Security
- `kaggle.json` is stored in `~/.kaggle/`
- File permissions are set to `600`
- The authenticated client is cached for the session

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
    st.markdown('<div class="main-title">📊 AI/ML DataSets EDA Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload CSV/Excel/JSON/TXT, paste a URL, or load a Kaggle dataset</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="badge-row">'
        '<span class="badge">CSV</span>'
        '<span class="badge">Excel</span>'
        '<span class="badge">JSON</span>'
        '<span class="badge">TXT</span>'
        '<span class="badge">🌐 Remote URL</span>'
        '<span class="badge">🏆 Kaggle</span>'
        '</div>',
        unsafe_allow_html=True
    )

    df = None
    input_name = "dataset"

    if "df_active" not in st.session_state:
        st.session_state.df_active = False

    if not st.session_state.df_active:
        f1, f2, f3 = st.columns(3)
        for i, (col, icon, title, desc) in enumerate([
            (f1, "📤", "1. Bring your data", "Drag & drop a file, paste a URL, or pull a dataset straight from Kaggle."),
            (f2, "⚙️", "2. Auto-profile", "One click runs a full statistical profile — types, missing values, correlations, distributions."),
            (f3, "📥", "3. Export & share", "Preview the interactive report in-app and download it as a standalone HTML file."),
        ]):
            col.markdown(
                f'<div class="feature-card" style="animation-delay:{i * 0.12}s">'
                f'<div class="icon">{icon}</div>'
                f'<div class="title">{title}</div>'
                f'<div class="desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.write("")

    st.markdown('<div class="section-title">Choose a data source</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📁 Upload File", "🌐 CSV URL", "🏆 Kaggle Dataset", "🔐 Kaggle Token"]
    )

    # ---- File Upload ----
    with tab1:
        st.markdown(
            '<div class="info-text">'
            'Supported formats: CSV (.csv), Excel (.xlsx, .xls), JSON (.json), TXT (.txt)<br>'
            'You can upload multiple files at once.'
            '</div>',
            unsafe_allow_html=True
        )

        uploaded_files = st.file_uploader(
            "Upload your file(s)",
            type=["csv", "xlsx", "xls", "json", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        if uploaded_files:
            csv_dfs = []
            other_dfs = []
            file_info = []

            for file in uploaded_files:
                df_temp = load_file(file)
                if df_temp is not None:
                    ext = Path(file.name).suffix.lower()
                    if ext == ".csv":
                        csv_dfs.append((file.name, df_temp))
                    else:
                        other_dfs.append((file.name, df_temp))
                    file_info.append({
                        "name": file.name,
                        "rows": len(df_temp),
                        "cols": len(df_temp.columns),
                        "type": ext.upper().lstrip('.')
                    })

            st.markdown("### 📋 Uploaded Files Summary")
            st.dataframe(pd.DataFrame(file_info), use_container_width=True)

            all_dfs = csv_dfs + other_dfs
            all_names = [name for name, _ in all_dfs]

            if all_dfs:
                mode = st.radio(
                    "How would you like to handle the uploaded files?",
                    ["📄 Analyze a single file", "📊 Generate EDA for each file separately"],
                    key="file_mode"
                )

                if mode == "📄 Analyze a single file":
                    selected_file = st.selectbox("Select file to analyze", all_names)
                    if selected_file:
                        df = dict(all_dfs)[selected_file]
                        input_name = sanitize_filename(selected_file)

                elif mode == "📊 Generate EDA for each file separately":
                    selected_files = st.multiselect(
                        "Select one or more files to generate EDA",
                        all_names,
                        default=all_names
                    )

                    if selected_files:
                        st.info("ℹ️ EDA reports will be generated one by one")
                        for fname in selected_files:
                            temp_df = dict(all_dfs)[fname]
                            st.markdown(f"### 📈 EDA for `{fname}`")
                            render_profile_report(
                                temp_df,
                                title=f"{fname} EDA Report",
                                download_label=f"⬇️ Download {fname} EDA",
                                file_name=f"{sanitize_filename(fname)}_eda.html"
                            )

    # ---- CSV URL ----
    with tab2:
        st.markdown(
            '<div class="info-text">'
            'Paste a CSV, TXT, Excel (.xlsx), GitHub file link, or Google Drive share link. '
            'Links are auto-converted.'
            '</div>',
            unsafe_allow_html=True
        )

        file_url = st.text_input(
            "Paste CSV / TXT / Excel / GitHub / Google Drive URL",
            placeholder="File link"
        )

        if file_url:
            try:
                original_url = file_url.strip()

                # ✅ GitHub blob → raw
                if "github.com" in original_url and "/blob/" in original_url:
                    file_url = original_url.replace(
                        "https://github.com/",
                        "https://raw.githubusercontent.com/"
                    ).replace("/blob/", "/")
                    st.info(f"🔁 GitHub link converted:\n{file_url}")

                # ✅ Google Drive → direct download
                elif "drive.google.com" in original_url:
                    match = re.search(r"/d/([a-zA-Z0-9_-]+)", original_url)
                    if match:
                        file_id = match.group(1)
                        file_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                        st.info(f"🔁 Google Drive link converted:\n{file_url}")
                    else:
                        st.error("❌ Invalid Google Drive link format")
                        file_url = None

                if file_url:
                    input_name = sanitize_filename(file_url)
                    lower_path = urlparse(file_url).path.lower()

                    response = requests.get(file_url, timeout=20)
                    response.raise_for_status()

                    if lower_path.endswith((".xlsx", ".xls")):
                        st.info("📊 Excel file detected")
                        df = pd.read_excel(BytesIO(response.content))

                    else:
                        content = response.text.strip()

                        # 🚫 HTML protection (e.g. Drive interstitial pages, dead links)
                        if "<html" in content[:1000].lower():
                            st.error(
                                "❌ The link does not provide raw data.\n\n"
                                "Make sure the file is public and is CSV, TXT, or Excel."
                            )
                        elif lower_path.endswith(".txt"):
                            try:
                                df = read_csv_robust(content, input_name)
                            except Exception:
                                df = pd.DataFrame({"text": content.splitlines()})
                        else:
                            df = load_csv_stringio(StringIO(content), file_url)

                    if df is not None:
                        st.success("✅ File loaded successfully")
                        st.markdown("### 📋 Uploaded Files Summary")
                        st.dataframe(
                            pd.DataFrame([{"name": input_name, "rows": len(df), "cols": len(df.columns)}]),
                            use_container_width=True
                        )

            except Exception as e:
                st.error(f"❌ Failed to load file: {e}")

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
                api = get_kaggle_api()
                kaggle_csv_files = download_kaggle_csvs(api, kaggle_dataset_name)
                csv_names = list(kaggle_csv_files.keys())

                st.success(f"✅ Found {len(csv_names)} CSV file(s)")

                file_info = []
                for csv_name in csv_names:
                    temp_df = load_path(kaggle_csv_files[csv_name])
                    if temp_df is not None:
                        file_info.append({
                            "name": csv_name,
                            "rows": len(temp_df),
                            "cols": len(temp_df.columns),
                            "type": "Kaggle CSV"
                        })

                st.markdown("### 📋 Dataset Files Summary")
                st.dataframe(pd.DataFrame(file_info), use_container_width=True)

                mode = st.radio(
                    "How would you like to handle the CSV files?",
                    [
                        "📄 Analyze a single CSV",
                        "🧩 Merge all CSVs (row-wise)",
                        "📊 Generate EDA for each CSV separately"
                    ]
                )

                if mode == "📄 Analyze a single CSV":
                    selected_csv = st.selectbox("Select CSV to analyze", csv_names)
                    if selected_csv:
                        df = load_path(kaggle_csv_files[selected_csv])
                        input_name = sanitize_filename(selected_csv)

                elif mode == "🧩 Merge all CSVs (row-wise)":
                    dfs = []
                    for csv_file in csv_names:
                        temp_df = load_path(kaggle_csv_files[csv_file])
                        if temp_df is not None:
                            temp_df["__source_file__"] = csv_file
                            dfs.append(temp_df)

                    if dfs:
                        df = pd.concat(dfs, ignore_index=True)
                        input_name = sanitize_filename(kaggle_dataset_name.replace("/", "_") + "_merged")
                        st.success("✅ All CSV files merged successfully")

                elif mode == "📊 Generate EDA for each CSV separately":
                    selected_csvs = st.multiselect(
                        "Select one or more CSV files",
                        csv_names,
                        default=csv_names
                    )

                    if selected_csvs:
                        st.info("ℹ️ EDA reports will be generated one by one")
                        for csv_file in selected_csvs:
                            temp_df = load_path(kaggle_csv_files[csv_file])
                            if temp_df is not None:
                                st.markdown(f"### 📈 EDA for `{csv_file}`")
                                render_profile_report(
                                    temp_df,
                                    title=f"{csv_file} EDA Report",
                                    download_label=f"⬇️ Download {csv_file} EDA",
                                    file_name=f"{sanitize_filename(csv_file)}_eda.html"
                                )

            except Exception as e:
                st.error(f"Kaggle download failed: {e}")

    # ---- Kaggle Token Upload ----
    with tab4:
        st.markdown('<div class="info-text">Upload your kaggle.json (only once, it will be saved locally)</div>', unsafe_allow_html=True)

        reauth = st.checkbox("Force re-authenticate Kaggle API")

        kaggle_file_uploaded = st.file_uploader(
            "Upload kaggle.json token",
            type=["json"],
            label_visibility="collapsed"
        )

        if kaggle_file_uploaded or reauth:
            try:
                if reauth:
                    get_kaggle_api.clear()
                get_kaggle_api(kaggle_file_uploaded.read() if kaggle_file_uploaded else None)
                st.success("✅ Kaggle API authenticated!")
            except Exception as e:
                st.error(f"Kaggle API setup failed: {e}")

        kaggle_file = Path.home() / ".kaggle" / "kaggle.json"
        if kaggle_file.exists():
            st.info("🔑 Kaggle token is already configured.")

    st.session_state.df_active = df is not None

    # ---------------- Data Preview & EDA ----------------
    if df is not None:
        with st.container(border=True):
            st.success("✅ Dataset Loaded Successfully")
            st.markdown(f"#### 👀 {input_name} Preview")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Rows", f"{len(df):,}")
            m2.metric("Columns", f"{df.shape[1]:,}")
            m3.metric("Missing cells", f"{df.isna().sum().sum():,}")
            m4.metric("Duplicate rows", f"{df.duplicated().sum():,}")

            st.dataframe(df.head(10), use_container_width=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate = st.button(
                "🚀 Generate EDA Report",
                use_container_width=True,
                type="primary"
            )

        if generate:
            st.markdown(
                f'<div class="eda-card"><h2>📈 {input_name} EDA Report Preview</h2></div>',
                unsafe_allow_html=True
            )
            with st.spinner("🔍 Generating EDA report..."):
                render_profile_report(
                    df,
                    title=f"{input_name} EDA Report",
                    download_label="⬇️ Download HTML Report",
                    file_name=f"{input_name}_eda.html",
                    height=1000
                )

    # ---------------- Footer with Contact Info ----------------
    st.markdown("""
    <hr style="border:1px solid rgba(255,255,255,0.1)">
    <div style="text-align:center; color:#a9adc1; font-size:0.9rem; margin-top:10px;">
    ⚡ Built with Streamlit • ydata-profiling • Kaggle API <br>
    📧 Contact: 2020tanvir1971@gmail.com | 📱 Phone: +88 0173837737
    </div>
    """, unsafe_allow_html=True)
