import streamlit as st
import numpy as np
import pandas as pd
import time
import altair as alt

st.title("Live Electricity Price – Streaming")

left, right = st.columns(2)

if "running" not in st.session_state:
    st.session_state.running = False

with left:
    if st.button("Start Simulation"):
        st.session_state.running = True
        
totalchange = np.random.uniform(-30, 40)
changestart = np.random.uniform(5, 20)
changeend = changestart + np.random.uniform(5, 20)
middle = (changestart + changeend) / 2
k = -np.log(1/0.99 - 1) / (changeend - middle)

with right:
    placeholder = st.empty()
    progress_bar = st.progress(0)

# ----------------------------
# STREAMING PARAMETERS
# ----------------------------
WINDOW_SECONDS = 15
DT = 0.2
Y_DOMAIN = [0, 90]
MAX_TIME = changeend + 4

# ----------------------------
# RUN SIMULATION
# ----------------------------
if st.session_state.running:
    times = []
    prices = []

    t = 0.0
    while t <= MAX_TIME:

        # --- price model ---
        if t < changestart:
            price = 40 + np.random.normal(0, 0.2)
        elif changestart <= t <= changeend:
            price = 40 + totalchange / (1 + np.exp(-k * (t - middle))) + np.random.normal(0, 0.2)
        else:
            price = 40 + totalchange + np.random.normal(0, 0.2)

        # --- append to stream ---
        times.append(t)
        prices.append(price)

        # --- streaming window ---
        window_start = max(0, t - WINDOW_SECONDS)
        mask = [ti >= window_start for ti in times]

        df = pd.DataFrame({
            "time": np.array(times)[mask],
            "price": np.array(prices)[mask]
        })

        # --- chart ---
        line = alt.Chart(df).mark_line(
            color="steelblue",
            strokeWidth=3
        ).encode(
            x=alt.X(
                "time:Q",
                scale=alt.Scale(domain=[window_start, window_start + WINDOW_SECONDS], nice=False),
                title="Time"
            ),
            y=alt.Y(
                "price:Q",
                scale=alt.Scale(domain=Y_DOMAIN, nice=False),
                title="Price (€/MWh)"
            )
        ).properties(
            height=400
        )

        latest_point = alt.Chart(df.tail(1)).mark_point(
            color="red",
            size=100
        ).encode(
            x="time:Q",
            y="price:Q"
        )

        chart = (line + latest_point).properties(
            title="Live Electricity Price (Streaming Window)"
        )

        placeholder.altair_chart(chart, use_container_width=True)

        # --- progress ---
        progress_bar.progress(int((t / MAX_TIME) * 100))

        time.sleep(0.05)
        t += DT

    st.success("✅ Simulation complete!")