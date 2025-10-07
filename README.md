# Kaggle Time Series Forecasting — Interactive Starter

This repo is a **ready-to-run time series forecasting project** you can use with popular Kaggle datasets (e.g., *Store Sales - Time Series Forecasting*, *Walmart Recruiting - Store Sales*, *Hourly Energy Consumption*, *M5 Forecasting*). It includes:

- An **interactive Streamlit app** for rapid exploration and forecasting
- A **CLI script** for batch training/evaluation on a CSV
- Clean, reusable **utility functions** for feature engineering & modeling (SARIMA / Auto-ARIMA)
- Clear instructions to reproduce results and write about it on your resume

> Bring your CSV from Kaggle, then run locally with Python — or deploy the app to Streamlit Cloud.

---

## 🧰 What you can do

- Upload a CSV, choose the **date** and **target** columns; optionally a **group** column (e.g., store, item).
- Auto-resample to daily/weekly/monthly frequency.
- Auto-train **Auto-ARIMA** (pmdarima) or a simple **baseline** (seasonal naive) as a comparison.
- Generate **forecasts** with **MAE / RMSE / MAPE** and **charts**.
- Save a **reproducible config** and **model** for later use.

---

## 📦 Quickstart

### 1) Create & activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) (Optional) Get your Kaggle CSV
Download a Kaggle dataset (e.g., sample sales.csv) and put it in the project folder. Typical minimum columns:
- `date` — timestamp or date string
- `y` — numeric target (e.g., sales)
- Optional: `group` — category to model separately (e.g., store_id)

You can **rename** your columns in-app if needed.

### 4) Run the interactive app
```bash
streamlit run streamlit_app.py
```

### 5) Or use the CLI
```bash
python -m src.train_cli --csv your_data.csv --date_col date --target_col y --horizon 28 --freq D
```

---

## 🧪 Suggested Kaggle datasets

- **Store Sales - Time Series Forecasting (Corporación Favorita)** — multi-store, multi-item demand
- **Walmart Recruiting - Store Sales Forecasting**
- **Hourly Energy Consumption (PJM)** — electricity load by region
- **M5 Forecasting** — hierarchical retail demand
- **Bitcoin Historical Data** — price time series

> Any dataset with a timestamp column and numeric target works.

---


---

## 📁 Repo structure

```
.
├── streamlit_app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── src
    ├── ts_utils.py
    └── train_cli.py
```

---

## 📝 Notes

- This starter avoids heavy dependencies (no Prophet by default) and keeps plots **matplotlib-only**.
- If your dataset is **hourly/minutely**, set `--freq H` or `--freq 15min` in the CLI or select in the app.
- For hierarchical datasets (store/item), start with per-group modeling (already supported) before moving to global models.
