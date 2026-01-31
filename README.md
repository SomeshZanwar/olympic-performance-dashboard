# Interactive Olympic Performance Analytics Dashboard

Streamlit dashboard exploring **120+ years of Olympic history** (1896–2016, 271k athlete records) with interactive filters and Plotly visualizations.[web:105]

## What this app does

- Summarizes Olympic KPIs: athletes, countries, sports, medals
- Lets you filter by **year, country, sport, medal type**
- Shows:
  - Top medal-winning countries
  - Country performance trends over time
  - Athlete age and physical profiles
  - Growth of events and participation

## Tech Stack

- Python, pandas, numpy
- Streamlit for UI
- Plotly for interactive charts
- Cached data loading for performance

## Project Structure


olympic-performance-dashboard/
├── data/
│   ├── raw/athlete_events.csv
│   └── processed/         # (optional, for future caching)
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── data_loader.py
├── app/
│   └── app.py
├── outputs/
│   └── figures/           # screenshots (for README)
├── README.md
├── requirements.txt
└── .gitignore 

## How to run localy

git clone https://github.com/<your-username>/olympic-performance-dashboard.git
cd olympic-performance-dashboard

python -m venv .venv
.venv/Scripts/Activate.ps1   # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

# Download athlete_events.csv from Kaggle:
# <https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results>[1]
# Place it at data/raw/athlete_events.csv

streamlit run app/app.py



 
