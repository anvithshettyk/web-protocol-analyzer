import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout="wide")
st.title("🚀 Advanced Network Analyzer")

API = "http://127.0.0.1:8000"

# 🌐 URL input
url = st.text_input("Enter Website (e.g. google.com)")

if st.button("Start Monitoring"):
    if url:
        requests.get(f"{API}/set_target?url={url}")

placeholder = st.empty()

while True:
    try:
        res = requests.get(f"{API}/data").json()
        df = pd.DataFrame(res["packets"])
        analysis = res["analysis"]

        with placeholder.container():

            col1, col2, col3 = st.columns(3)

            # 📊 Protocols
            with col1:
                if analysis:
                    fig = px.pie(
                        values=list(analysis["protocol_count"].values()),
                        names=list(analysis["protocol_count"].keys()),
                        title="Protocols"
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # 📈 Speed Graph
            with col2:
                if analysis:
                    speed_df = pd.DataFrame({
                        "time": list(analysis["speed_series"].keys()),
                        "bytes": list(analysis["speed_series"].values())
                    })
                    fig2 = px.line(speed_df, x="time", y="bytes", title="Live Speed")
                    st.plotly_chart(fig2, use_container_width=True)

            # 🌍 Domains
            with col3:
                if analysis:
                    fig3 = px.bar(
                        x=list(analysis["top_domains"].keys()),
                        y=list(analysis["top_domains"].values()),
                        title="Top Domains"
                    )
                    st.plotly_chart(fig3, use_container_width=True)

            # 🚨 Alert
            if analysis.get("anomalies"):
                st.error("⚠️ High Traffic Detected!")

            # 📊 Metrics
            c1, c2 = st.columns(2)
            c1.metric("Total Data", analysis.get("total_bytes", 0))
            c2.metric("Speed (bytes/sec)", analysis.get("speed", 0))

            st.subheader("📄 Live Packet Data")
            st.dataframe(df.tail(20), use_container_width=True)

    except:
        st.warning("Waiting for backend...")

    time.sleep(2)