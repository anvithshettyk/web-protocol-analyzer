from fastapi import FastAPI
from sniffer import start_sniffing, get_packets, set_target
from analyzer import analyze
import threading

app = FastAPI()

threading.Thread(target=start_sniffing, daemon=True).start()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/set_target")
def set_target_url(url: str):
    set_target(url)
    return {"message": f"Tracking {url}"}

@app.get("/data")
def get_data():
    packets = get_packets()
    return {
        "packets": packets,
        "analysis": analyze(packets)
    }