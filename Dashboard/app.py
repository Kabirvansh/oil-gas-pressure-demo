import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Compressor Station Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = pd.read_csv("Dashboard/data/pressure_log.csv", parse_dates=["timestamp"])

st.sidebar.header("Filters & Options")
show_data = st.sidebar.checkbox("Show raw data", value=False)
time_range = st.sidebar.slider(
    "Select time range (minutes):",
    min_value=1, max_value=10, value=(1, 10)
)
start, end = df["timestamp"].min(), df["timestamp"].max()
mask = (df["timestamp"] >= start + pd.Timedelta(minutes=time_range[0]-1)) & \
       (df["timestamp"] <= start + pd.Timedelta(minutes=time_range[1]-1))
filtered = df.loc[mask]

st.title("🛢️ Compressor Station Dashboard")
st.markdown(
    """
    **Interactive visualization** of inlet/outlet pressures and alarm events  
    Built with Streamlit • Data simulated from SCADA logs
    """
)

st.subheader("Pressure Over Time (psi)")
pressure_df = filtered.set_index("timestamp")[["inlet", "outlet"]]
st.line_chart(pressure_df, height=350)

st.subheader("Alarm Occurrences")
alarm_counts = filtered["alarm"].value_counts().sort_index()
alarm_counts.index = alarm_counts.index.map({0: "Normal", 1: "Alarm"})
st.bar_chart(alarm_counts, height=250)

if show_data:
    st.subheader("Raw SCADA Log Data")
    st.dataframe(filtered.style.format({
        "inlet": "{:.1f}",
        "outlet": "{:.1f}"
    }))

st.markdown(
    """
    ---
    **Project:** Oil & Gas Compressor Station SCADA Demo •  
    **Repo:** https://github.com/yourusername/oilandgas-pressure-demo  
    """
)
