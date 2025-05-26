import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="SCADA Alarm Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("SCADA Alarm & Pressure Dashboard")
uploaded = st.sidebar.file_uploader("Upload CSV file(beta)", type="csv")

if uploaded:
    df = pd.read_csv(uploaded, parse_dates=["timestamp"])
else:
    st.sidebar.info("Using built-in sample data.")
    df = pd.read_csv("Dashboard/data/pressure_log.csv", parse_dates=["timestamp"])

df.sort_values("timestamp", inplace=True)

st.sidebar.markdown("### Filters")

df["timestamp"] = pd.to_datetime(df["timestamp"])
min_time = df["timestamp"].min().to_pydatetime()
max_time = df["timestamp"].max().to_pydatetime()
start, end = st.sidebar.slider(
    "Select Time Range:",
    min_value=min_time,
    max_value=max_time,
    value=(min_time, max_time),
    format="YYYY-MM-DD HH:mm:ss"
)
df = df[(df["timestamp"] >= pd.to_datetime(start)) & (df["timestamp"] <= pd.to_datetime(end))]

tabs = st.tabs(["Trends", "Distribution", "Details"])

with tabs[0]:
    st.subheader("Alarm & Pressure Trends Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["alarm"], mode='lines+markers', name='Alarms',
        line=dict(width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["inlet"], mode='lines', name='Inlet Pressure'
    ))
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["outlet"], mode='lines', name='Outlet Pressure'
    ))
    fig.update_layout(
        xaxis=dict(range=[start, end], rangeslider=dict(visible=True)),
        yaxis_title="Value",
        legend_title="Series",
        hovermode="x unified",
        title="Time-Series with Range Slider"
    )
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Alarm State Breakdown")
        dist = df['alarm'].value_counts().rename(index={0: 'Normal', 1: 'Alarm'})
        fig1 = px.pie(
            names=dist.index, values=dist.values,
            title="Normal vs Alarm %",
            hole=0.4
        )
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader("Pressure Distributions")
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(x=df['inlet'], nbinsx=30, name='Inlet', opacity=0.7))
        fig2.add_trace(go.Histogram(x=df['outlet'], nbinsx=30, name='Outlet', opacity=0.7))
        fig2.update_layout(barmode='overlay', title="Inlet & Outlet Pressure Histograms")
        st.plotly_chart(fig2, use_container_width=True)

with tabs[2]:
    st.subheader("Alarm Events Table")
    st.dataframe(df[df['alarm'] == 1].reset_index(drop=True), use_container_width=True)
    st.markdown("---")
    st.subheader("Correlation Heatmap")
    corr = df[['alarm', 'inlet', 'outlet']].corr()
    fig3 = px.imshow(
        corr, text_auto=True, aspect='auto',
        title='Correlation Matrix'
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.caption(f"Data from {df['timestamp'].min()} to {df['timestamp'].max()} | Total points: {len(df)}")
