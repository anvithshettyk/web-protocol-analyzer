import pandas as pd
import time

start_time = time.time()

def analyze(data):
    df = pd.DataFrame(data)

    if df.empty:
        return {}

    total_bytes = df["size"].sum()
    duration = time.time() - start_time
    speed = total_bytes / duration if duration > 0 else 0

    df["time"] = pd.to_datetime(df["time"])
    speed_series = df.groupby(df["time"].dt.second)["size"].sum()

    avg = speed_series.mean()
    anomalies = speed_series[speed_series > avg * 2]

    return {
        "protocol_count": df["protocol"].value_counts().to_dict(),
        "bandwidth": df.groupby("protocol")["size"].sum().to_dict(),
        "top_domains": df["domain"].value_counts().head(5).to_dict(),
        "speed": round(speed, 2),
        "total_bytes": int(total_bytes),
        "speed_series": speed_series.to_dict(),
        "anomalies": anomalies.to_dict()
    }