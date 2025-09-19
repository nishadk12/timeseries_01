# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from src.ts_utils import TSConfig, load_csv, run_single_series, run_grouped
import io
import base64
import yaml

st.set_page_config(page_title="Time Series Forecasting (Kaggle-ready)", layout="wide")

st.title("🕒 Time Series Forecasting — Kaggle-ready Interactive App")

with st.sidebar:
    st.header("1) Upload CSV")
    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])
    st.caption("Tip: Export a Kaggle dataset CSV with a date column and numeric target.")

    st.header("2) Columns & Settings")
    date_col = st.text_input("Date column name", value="date")
    target_col = st.text_input("Target column (numeric)", value="y")
    group_col = st.text_input("Group column (optional, e.g., store)", value="")
    freq = st.selectbox("Resample frequency", options=["(none)", "D", "W", "M", "H"], index=1)
    horizon = st.number_input("Forecast horizon (steps)", value=28, min_value=1, step=1)
    m = st.number_input("Seasonal period m (e.g., 7 for daily weekly-seasonality)", value=7, min_value=1, step=1)
    seasonal = st.checkbox("Use seasonal ARIMA", value=True)

    st.header("3) Run")
    run_btn = st.button("Train & Forecast")

    st.markdown("---")
    st.header("Export Config")
    if st.button("Download current config YAML"):
        cfg = {
            "date_col": date_col,
            "target_col": target_col,
            "group_col": group_col or None,
            "freq": None if freq == "(none)" else freq,
            "horizon": int(horizon),
            "test_size": 0.2,
            "seasonal": seasonal,
            "m": int(m),
        }
        yaml_bytes = yaml.dump(cfg).encode("utf-8")
        st.download_button("Save config.yaml", yaml_bytes, file_name="config.yaml")

main_tab, metrics_tab = st.tabs(["📈 Forecast", "📊 Metrics JSON"])

if run_btn and uploaded is not None:
    csv_bytes = uploaded.read()
    tmp_path = "uploaded.csv"
    with open(tmp_path, "wb") as f:
        f.write(csv_bytes)

    cfg = TSConfig(
        date_col=date_col,
        target_col=target_col,
        group_col=group_col or None,
        freq=None if freq == "(none)" else freq,
        horizon=int(horizon),
        test_size=0.2,
        seasonal=seasonal,
        m=int(m),
    )

    try:
        df = load_csv(tmp_path, cfg)
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        st.stop()

    if cfg.group_col and cfg.group_col in df.columns:
        results = run_grouped(df, cfg)
        with main_tab:
            st.subheader("Per-group metrics (ARIMA vs baseline)")
            st.dataframe(pd.DataFrame(results).T)
        with metrics_tab:
            st.json(results)
    else:
        out = run_single_series(df[[cfg.date_col, cfg.target_col]].reset_index(drop=True), cfg)
        with main_tab:
            st.subheader("Forecast Plot")
            st.image(out["plot_png"])
            st.caption("Train (left), Test (right), Forecast (overlay).")

        with metrics_tab:
            st.json({
                "baseline_metrics": out["baseline_metrics"],
                "arima_metrics": out["arima_metrics"],
            })

else:
    with main_tab:
        st.info("Upload a CSV, set columns, and click **Train & Forecast** in the sidebar.")

st.markdown("---")
st.caption("Tip: Try with Kaggle datasets such as Store Sales, Walmart Store Sales, M5, PJM Hourly Energy.")
