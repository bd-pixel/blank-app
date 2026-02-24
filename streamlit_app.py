import streamlit as st
import numpy as np
import pandas as pd
import time

st.title("Live Electricity Price")

# Split the layout into two columns
left, right = st.columns(2)

# Initialize session state
if "running" not in st.session_state:
    st.session_state.running = False

# Place the button in the left column
with left:
    if st.button("Start Simulation"):
        st.session_state.running = True
        totalchange = np.random.uniform(-30, 40)
        changestart = np.random.uniform(5, 20)
        changeend = changestart + np.random.uniform(5, 20)
        middle = (changestart + changeend) / 2
        k = -np.log(1/0.99 - 1) / (changeend - middle)

# Place the chart in the right column
with right:
    placeholder = st.empty()

if st.session_state.running:
    # Initialize DataFrame
    df = pd.DataFrame(columns=["time", "price"])

    for t in np.arange(0, changeend + 4, 0.5):  # Larger step for smoother mobile updates
        if t < changestart:
            price = 40 + np.random.uniform(-0.2, 0.2)
            if changestart - t < 5:
                price = 40 + totalchange/8 * np.sin(np.random.normal(0, 1)/5) + np.random.normal(0, 0.2)
        elif t > changestart and t < changeend:
            price = 40 + (totalchange / (1 + np.exp(-k * (t - middle)))) + np.random.uniform(-0.2, 0.2)
        else:
            price = 40 + totalchange + np.random.uniform(-0.2, 0.2)

        # Append new data
        new_row = {"time": t, "price": price}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Update the chart
        with right:
            placeholder.line_chart(df, x="time", y="price", use_container_width=True)

        time.sleep(0.05)  # Slower updates for mobile

    st.success("✅ Simulation complete!")
