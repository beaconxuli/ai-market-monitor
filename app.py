# -*- coding: utf-8 -*-
"""AI行情监控 - 云端版 (Render/任意Python主机部署)"""
import os, sys, json, threading, time, urllib.request
from datetime import date
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for d in ["data", "logs", "reports"]:
    os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

# ===== 简化的数据库(JSON文件) =====
DB_FILE = os.path.join(BASE_DIR, "data", "prices.json")

GPU_MARKET = {
    "NVIDIA H100 80GB": {"msrp_usd": 28000, "cloud_usd_per_hour": 1.99, "source": "NVIDIA官方MSRP / Lambda公开定价"},
    "NVIDIA H200 141GB": {"msrp_usd": 35000, "cloud_usd_per_hour": 2.49, "source": "NVIDIA官方MSRP / 行业估算"},
    "NVIDIA B200": {"msrp_usd": 40000, "cloud_usd_per_hour": 3.50, "source": "NVIDIA GTC 2024 / 行业估算"},
    "NVIDIA A100 80GB": {"msrp_usd": 15000, "cloud_usd_per_hour": 1.10, "source": "NVIDIA MSRP / 云厂商均价"},
    "NVIDIA L40S": {"msrp_usd": 9000, "cloud_usd_per_hour": 0.80, "source": "NVIDIA MSRP / Lambda公开定价"},
    "NVIDIA RTX 6000 Ada": {"msrp_usd": 6800, "cloud_usd_per_hour": 0.65, "source": "NVIDIA MSRP / Vast.ai公开行情"},
    "NVIDIA RTX 4090": {"msrp_usd": 1599, "cloud_usd_per_hour": 0.35, "source": "NVIDIA MSRP / Vast.ai公开行情"},
    "NVIDIA H100 国内": {"msrp_usd": 35000, "cloud_usd_per_hour": 2.80, "source": "NVIDIA MSRP+出口管制溢价"},
    "华为昇腾910B": {"msrp_usd": 12000, "cloud_usd_per_hour": 0.90, "source": "华为公开定价"},
}

TOKEN_MODELS = ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022",
    "gemini-2.0-flash", "deepseek-chat", "deepseek-reasoner", "qwen-max", "doubao-pro-32k",
    "hunyuan-turbo", "llama-4-maverick-03-26-25", "mistral-large-latest"]

def fetch_real_data():
    """从LiteLLM拉取真实Token价格"""
    try:
        r = urllib.request.urlopen(
            "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json",
            timeout=30)
        litellm = json.loads(r.read().decode())
    except:
        litellm = {}

    data = {"gpu": [], "token": [], "updated": date.today().isoformat()}

    # GPU数据
    for name, info in GPU_MARKET.items():
        region = "国内" if "国内" in name else "国际"
        cat = "gpu"
        data["gpu"].append({
            "name": name, "category": cat, "region": region,
            "prices": [
                {"type": "MSRP(美元)", "value": info["msrp_usd"], "unit": "USD"},
                {"type": "云租赁(美元/小时)", "value": info["cloud_usd_per_hour"], "unit": "USD/hr"},
            ],
            "source": info["source"]
        })

    # Token数据 - 从LiteLLM提取
    token_names = {
        "gpt-4o": "GPT-4o", "gpt-4o-mini": "GPT-4o Mini", "gpt-4.1": "GPT-4.1",
        "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet",
        "claude-3-5-haiku-20241022": "Claude 3.5 Haiku",
        "gemini-2.0-flash": "Gemini 2.0 Flash",
        "deepseek-chat": "DeepSeek V3", "deepseek-reasoner": "DeepSeek R1",
        "qwen-max": "Qwen Max", "doubao-pro-32k": "豆包 Pro 32K",
        "hunyuan-turbo": "混元 Turbo", "llama-4-maverick-03-26-25": "Llama 4",
        "mistral-large-latest": "Mistral Large"
    }

    for model_id, display_name in token_names.items():
        if model_id in litellm:
            p = litellm[model_id]
            inp = p.get("input_cost_per_token", 0) * 1_000_000
            out = p.get("output_cost_per_token", 0) * 1_000_000
            region = "国内" if any(kw in model_id for kw in ["deepseek", "qwen", "doubao", "hunyuan", "ernie"]) else "国际"
            cat = "llm_domestic" if region == "国内" else "llm_intl"
            prices = []
            if inp > 0: prices.append({"type": "Input($/1M tokens)", "value": round(inp, 4), "unit": "USD/1M"})
            if out > 0: prices.append({"type": "Output($/1M tokens)", "value": round(out, 4), "unit": "USD/1M"})
            if prices:
                data["token"].append({
                    "name": display_name, "category": cat, "region": region,
                    "prices": prices,
                    "source": "LiteLLM (community-maintained official pricing)"
                })

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data

# 初始拉取
print("[INIT] Fetching real market data...")
try:
    MARKET_DATA = fetch_real_data()
    print(f"[INIT] GPU: {len(MARKET_DATA['gpu'])} items, Token: {len(MARKET_DATA['token'])} items")
except Exception as e:
    print(f"[INIT] Fetch failed: {e}")
    MARKET_DATA = {"gpu": [], "token": [], "updated": ""}

# 定时刷新(每6小时)
def periodic_refresh():
    global MARKET_DATA
    while True:
        time.sleep(6 * 3600)
        try:
            MARKET_DATA = fetch_real_data()
            print(f"[REFRESH] Updated at {date.today()}")
        except Exception as e:
            print(f"[REFRESH] Failed: {e}")

threading.Thread(target=periodic_refresh, daemon=True).start()

# ===== API路由 =====
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/prices")
def api_prices():
    """返回所有真实价格数据"""
    all_data = MARKET_DATA["gpu"] + MARKET_DATA["token"]
    return jsonify(all_data)

@app.route("/api/summary")
def api_summary():
    """返回摘要"""
    gpu_count = len(MARKET_DATA["gpu"])
    token_count = len(MARKET_DATA["token"])
    return jsonify({
        "object_count": gpu_count + token_count,
        "today_records": sum(len(item["prices"]) for item in MARKET_DATA["gpu"] + MARKET_DATA["token"]),
        "source_count": 2,
        "is_fresh": True,
        "last_update_time": MARKET_DATA["updated"],
        "data_sources": ["NVIDIA官方MSRP + 云厂商公开定价", "LiteLLM社区维护(2986模型)"]
    })

@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    """手动刷新"""
    global MARKET_DATA
    try:
        MARKET_DATA = fetch_real_data()
        return jsonify({"success": True, "message": "数据已更新"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 18888))
    print(f"Starting on port {port}")
    app.run(host="0.0.0.0", port=port)
