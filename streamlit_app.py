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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines"))

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Price (ct/kWh)",
        yaxis_range=[0, 90],
    )

    data_x = []
    data_y = []

    shock_minute = 50

    for minute in range(90):

        if minute < shock_minute:
            price = 40 + np.random.normal(0, 0.2)
        else:
            price = 75 + np.random.normal(0, 0.5)

        data_x.append(minute)
        data_y.append(price)

        fig.data[0].x = data_x
        fig.data[0].y = data_y

        placeholder.plotly_chart(fig, use_container_width=True)

        time.sleep(0.01)