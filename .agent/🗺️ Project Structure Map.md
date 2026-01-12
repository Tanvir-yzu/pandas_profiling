# Project Structure Map

## Overview
This document provides a detailed map of the project structure for the **Streamlit Auto-EDA App**, describing all main directories, subdirectories, key files, their purposes, interactions, and dependencies. It serves as a reference for developers joining or working on the project.

## Root Directory
```
Streamlit Auto-EDA app/
├── app.py
├── kaggle.json.py
├── requirements.txt
├── README.MD
├── .gitignore
├── myenv/               # Python virtual environment (excluded from repo)
└── .agent/              # Internal project governance & documentation
    ├── 📝 Coding Standards & Agent Behavior.md
    ├── 📋 Code Review Workflow.md
    └── 🗺️ Project Structure Map.md
```

---

## Key Files & Purposes

### `/app.py`
- **Purpose**: Main entry point of the Streamlit web application.
- **Contains**: UI layout, user input handling, data processing logic, integration with `ydata-profiling`, custom CSS for modern UI (neumorphism, gradients, responsive design).
- **Interactions**:
  - Reads uploaded datasets (CSV, Excel).
  - Triggers exploratory data analysis (EDA) generation.
  - Displays results using Streamlit components and embedded profiling reports.
- **Dependencies**: `streamlit`, `pandas`, `ydata-profiling`, `openpyxl`/`xlrd`.

### `/kaggle.json.py`
- **Purpose**: Template or helper script for managing Kaggle API credentials securely.
- **Contains**: Instructions/structure for placing `kaggle.json` and preventing accidental commits.
- **Dependencies**: None at runtime (used for configuration).

### `/requirements.txt`
- **Purpose**: Lists Python package dependencies with pinned versions.
- **Contains**: `streamlit`, `pandas`, `ydata-profiling`, plus extras for Excel support.
- **Role**: Ensures reproducible environment setup (`pip install -r requirements.txt`).

### `/README.MD`
- **Purpose**: Project documentation for installation, usage, design system, configuration, troubleshooting, and structure.
- **Interactions**: Referenced by developers/users for onboarding and operational guidance.

### `/.gitignore`
- **Purpose**: Specifies files/folders excluded from version control.
- **Covers**: Python cache (`__pycache__`, `*.pyc`), virtual environment (`myenv/`), IDE settings, data files, secrets.

### `/myenv/`
- **Purpose**: Local Python virtual environment (created via `python -m venv myenv`).
- **Excluded from Git**: Prevents environment-specific files in repo.

---

## `.agent/` Directory (Governance & Documentation)
- **Purpose**: Central location for project process documents and standards.
- **Components**:
  1. **📝 Coding Standards & Agent Behavior.md**
     - Defines language consistency rules and behavior pattern modeling/testing/documentation guidelines.
  2. **📋 Code Review Workflow.md**
     - Describes stages of code review: setup, automated checks, manual review, feedback loop, merge.
  3. **🗺️ Project Structure Map.md** *(this file)*
     - Provides structural overview and module relationships.

---

## Module Interactions & Dependencies

1. **User ↔ app.py**
   - User interacts via Streamlit UI (file upload, button clicks).
   - `app.py` processes inputs, runs analysis, renders output.

2. **app.py ↔ pandas**
   - Data ingestion and manipulation using DataFrames.

3. **app.py ↔ ydata-profiling**
   - Generates comprehensive EDA reports from DataFrames.

4. **app.py ↔ Streamlit Components**
   - Uses built-in widgets (file_uploader, button, spinner, success/error boxes) for UI/UX.

5. **app.py ↔ Custom CSS (embedded)**
   - Enhances visual design (gradients, shadows, neumorphism, responsive layouts).

6. **requirements.txt ↔ Environment**
   - All Python dependencies declared here are installed into `myenv` or deployment environment.

7. **README.MD ↔ All Modules**
   - Documents how to set up and use each component.

8. **.gitignore ↔ All Directories/Files**
   - Ensures separation of source code from transient/dev-specific files.

9. **.agent/ Docs ↔ Development Process**
   - Standards and workflows guide contributors on code quality, reviews, and structure comprehension.

---

## Dependency Graph (Logical)
```
User → Streamlit UI (app.py) → pandas → ydata-profiling → Report
                                    ↘
                                     Custom CSS (UI styling)
requirements.txt → myenv (runtime)
.gitignore → excludes myenv/, __pycache__/, secrets
README.MD → describes all above
.agent/ → enforces standards & workflow
```

---

## Notes for Developers
- Keep `myenv/` excluded from version control.
- Place API keys/secrets outside repo; reference via environment variables or config templates (`kaggle.json.py`).
- Follow behavior modeling & testing guidelines from `.agent/📝 Coding Standards & Agent Behavior.md`.
- Adhere to review workflow in `.agent/📋 Code Review Workflow.md` for all contributions.
- Update this map when adding major modules or changing dependencies.
