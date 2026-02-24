import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.title("Live Electricity Price")

if "running" not in st.session_state:
    st.session_state.running = False

if st.button("Start Simulation"):
    st.session_state.running = True

if st.session_state.running:

    placeholder = st.empty()

    # Create figure ONCE
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[],
            y=[],
            mode="lines",
            line=dict(width=3),
        )
    )

    # 🔥 Critical: lock axis ranges (prevents jitter)
    fig.update_layout(
        #xaxis=dict(range=[0, 60], fixedrange=True),
        yaxis=dict(range=[30, 90], fixedrange=True),
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
    )

    data_x = []
    data_y = []

    shock_time = 35

    for t in np.arange(0, 60, 0.2):  # small step = smooth movement

        if t < shock_time:
            price = 40 + np.random.normal(0, 0.15)
        else:
            price = 75 + np.random.normal(0, 0.4)

        data_x.append(t)
        data_y.append(price)

        # Only update trace data (not figure layout)
        fig.data[0].x = data_x
        fig.data[0].y = data_y

        placeholder.plotly_chart(
            fig,
            width="stretch",
            config={"scrollZoom": False},
        )

        time.sleep(0.01)  # lower = smoother (but more CPU)

    st.error("⚠️ Price Surge Detected")