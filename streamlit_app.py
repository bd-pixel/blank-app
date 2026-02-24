import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.title("Live Electricity Price")

# Split the layout into two equal columns
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

# Place the plot in the right column
with right:
    placeholder = st.empty()

if st.session_state.running:
    # Create figure and trace ONCE
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[],
            y=[],
            mode="lines",
            line=dict(width=4, color="blue"),
        )
    )

    # Lock axis ranges
    fig.update_layout(
        yaxis=dict(range=[0, 90], fixedrange=True),
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
    )

    data_x = []
    data_y = []

    for t in np.arange(0, changeend + 4, 0.1):
        if t < changestart:
            price = 40 + np.random.uniform(-0.2, 0.2)
            if changestart - t < 5:
                price = 40 + totalchange/8 * np.sin(np.random.normal(0, 1)/5) + np.random.normal(0, 0.2)
        elif t > changestart and t < changeend:
            price = 40 + (totalchange / (1 + np.exp(-k * (t - middle)))) + np.random.uniform(-0.2, 0.2)
        else:
            price = 40 + totalchange + np.random.uniform(-0.2, 0.2)

        data_x.append(t)
        data_y.append(price)

        # Update only the data, not the entire figure
        fig.data[0].x = data_x
        fig.data[0].y = data_y

        if t > changestart and t < changeend and len(data_y) > 5:
            if price > max(data_y[-5:]):
                fig.data[0].line.color = "red"  # increasing
            elif price < min(data_y[-5:]):
                fig.data[0].line.color = "green"  # decreasing
            else:
                fig.data[0].line.color = "blue"  # neutral

        with right:
            placeholder.plotly_chart(
                fig,
                use_container_width=True,
                config={"scrollZoom": False},
            )

        time.sleep(0.01)

    st.error("⚠️ Price Surge Detected")
