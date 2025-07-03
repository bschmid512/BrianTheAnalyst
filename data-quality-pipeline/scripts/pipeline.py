#!/usr/bin/env python3
import pandas as pd
import glob, os, datetime
from jinja2 import Environment, FileSystemLoader

# 1) config paths
RAW_DIR    = '../data/raw'
CLEAN_DIR  = '../data/clean'
REPORT_DIR = '../data/reports'
TEMPLATE   = 'report_template.html'

os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# 2) validation rules
def validate(df):
    issues = []
    # a) missing values
    na = df.isna().sum().sum()
    if na:
        issues.append(f'{na} missing values detected')
    # b) typical ranges (example columns)
    ranges = {
        'wind_speed': (0, 30),
        'power': (0, 2300),  # kW, turbine rating
        'rotor_speed': (0, 25)
    }
    for col,(low,high) in ranges.items():
        if col in df:
            bad = df[(df[col] < low) | (df[col] > high)]
            if not bad.empty:
                issues.append(f'{len(bad)} rows out of range in "{col}"')
    return issues

# 3) process each raw file
reports = []
for path in sorted(glob.glob(f'{RAW_DIR}/*.csv')):
    fname   = os.path.basename(path)
    df      = pd.read_csv(path, parse_dates=['timestamp'])
    issues  = validate(df)
    # drop bad rows (simple example: drop any row with NA)
    df_clean = df.dropna()
    clean_path = os.path.join(CLEAN_DIR, fname)
    df_clean.to_csv(clean_path, index=False)
    # collect report data
    reports.append({
        'file': fname,
        'rows_raw': len(df),
        'rows_clean': len(df_clean),
        'issues': issues
    })

# 4) render HTML report
env      = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
template = env.get_template(TEMPLATE)
html     = template.render(
    generated_at = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
    reports      = reports
)
outpath  = os.path.join(REPORT_DIR, f'qc_report_{datetime.date.today()}.html')
with open(outpath, 'w') as f:
    f.write(html)
print(f'Report written to {outpath}')
