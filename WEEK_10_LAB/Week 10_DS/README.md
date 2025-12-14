Running the Week 10 Streamlit app

Prerequisites:
- Python 3.8+ installed

Quick Steps (PowerShell):

```powershell
# 1. Create and activate venv
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Run the streamlit app
streamlit run Home.py
```

Notes:
- Run `streamlit run Home.py` from this folder so the `app` package resolves correctly.
- If you get ModuleNotFoundError: No module named 'plotly' or similar, install missing packages with `pip install package_name` or re-run the `pip install -r requirements.txt` command.
- Windows: if `bcrypt` fails to install, ensure Build Tools are available or try `pip install bcrypt` after installing the Microsoft C++ Build Tools.
