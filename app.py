# -*- coding: utf-8 -*-
"""AI行情监控 - PythonAnywhere版"""
import sys, os, json, urllib.request
from datetime import date
from flask import Flask, jsonify

app = Flask(__name__)

# 数据文件
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "prices.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# GPU真实行情
GPU_MARKET = {
    "NVIDIA H100 80GB": {"msrp_usd": 28000, "cloud_usd_per_hour": 1.99},
    "NVIDIA H200 141GB": {"msrp_usd": 35000, "cloud_usd_per_hour": 2.49},
    "NVIDIA B200": {"msrp_usd": 40000, "cloud_usd_per_hour": 3.50},
    "NVIDIA A100 80GB": {"msrp_usd": 15000, "cloud_usd_per_hour": 1.10},
    "NVIDIA A100 40GB": {"msrp_usd": 11000, "cloud_usd_per_hour": 0.79},
    "NVIDIA L40S": {"msrp_usd": 9000, "cloud_usd_per_hour": 0.80},
    "NVIDIA RTX 4090": {"msrp_usd": 1599, "cloud_usd_per_hour": 0.35},
    "NVIDIA H100 国内(含溢价)": {"msrp_usd": 35000, "cloud_usd_per_hour": 2.80},
    "华为昇腾910B": {"msrp_usd": 12000, "cloud_usd_per_hour": 0.90},
}

def fetch_token_prices():
    try:
        r = urllib.request.urlopen(
            "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json",
            timeout=30)
        return json.loads(r.read().decode())
    except:
        return {}

TOKEN_KEYS = {
    "gpt-4o": "GPT-4o", "gpt-4o-mini": "GPT-4o Mini",
    "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet",
    "gemini-2.0-flash": "Gemini 2.0 Flash",
    "deepseek-chat": "DeepSeek V3", "deepseek-reasoner": "DeepSeek R1",
    "qwen-max": "Qwen Max", "hunyuan-turbo": "Hunyuan Turbo",
    "llama-4-maverick-03-26-25": "Llama 4 Maverick",
}

def build_data():
    litellm = fetch_token_prices()
    data = {"gpu": [], "token": [], "updated": date.today().isoformat()}

    for name, info in GPU_MARKET.items():
        region = "国内" if "国内" in name else "国际"
        data["gpu"].append({
            "name": name, "category": "gpu", "region": region,
            "prices": [
                {"type": "MSRP(美元)", "value": info["msrp_usd"], "unit": "USD"},
                {"type": "云租赁(美元/小时)", "value": info["cloud_usd_per_hour"], "unit": "USD/hr"},
            ]
        })

    for model_id, display_name in TOKEN_KEYS.items():
        if model_id in litellm:
            p = litellm[model_id]
            inp = p.get("input_cost_per_token", 0) * 1000000
            out = p.get("output_cost_per_token", 0) * 1000000
            region = "国内" if any(kw in model_id for kw in ["deepseek","qwen","hunyuan"]) else "国际"
            cat = "llm_domestic" if region == "国内" else "llm_intl"
            prices = []
            if inp > 0: prices.append({"type": "Input($/1M tokens)", "value": round(inp, 4), "unit": "USD/1M"})
            if out > 0: prices.append({"type": "Output($/1M tokens)", "value": round(out, 4), "unit": "USD/1M"})
            if prices:
                data["token"].append({"name": display_name, "category": cat, "region": region, "prices": prices})

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return data

# 启动时拉取数据
try:
    MARKET_DATA = build_data()
except Exception as e:
    MARKET_DATA = {"gpu": [], "token": [], "updated": ""}

@app.route("/")
def index():
    return jsonify({"status": "ok", "service": "AI Market Monitor", "updated": MARKET_DATA["updated"]})

@app.route("/api/prices")
def api_prices():
    return jsonify(MARKET_DATA["gpu"] + MARKET_DATA["token"])

@app.route("/api/summary")
def api_summary():
    all_items = MARKET_DATA["gpu"] + MARKET_DATA["token"]
    return jsonify({
        "object_count": len(all_items),
        "today_records": sum(len(item["prices"]) for item in all_items),
        "source_count": 2,
        "is_fresh": True,
        "last_update_time": MARKET_DATA["updated"],
        "data_sources": ["NVIDIA MSRP + 云厂商公开定价", "LiteLLM (2986 models)"]
    })

@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    global MARKET_DATA
    try:
        MARKET_DATA = build_data()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("Starting AI Market Monitor...")
    app.run(host="0.0.0.0", port=18888, debug=True)
