# SOP: Onboard a New SCADA Site

## 1. Drop Raw File  
Place the daily SCADA export CSV into `data/raw/` named `site_<YYYYMMDD>.csv`.

## 2. Run the Pipeline  
Manually (optional) or wait for GitHub Actions to run nightly.

```bash
pip install -r requirements.txt
python scripts/pipeline.py
