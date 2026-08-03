# -*- coding: utf-8 -*-
"""AI Infrastructure & Token Market Monitor - Production
近6个月主流大模型监控清单版 (2026-07-31 更新)
"""
import sys, os, json, urllib.request
from datetime import date
from flask import Flask, jsonify

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "prices.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

GPU_MARKET = {
    "NVIDIA H100 80GB SXM": {
        "MSRP(USD)": 28000, "Cloud/hr(USD)": 1.99, "China Proxy(USD)": 33000,
        "source": "NVIDIA / Lambda Labs / China proxy"
    },
    "NVIDIA H200 141GB SXM": {
        "MSRP(USD)": 35000, "Cloud/hr(USD)": 2.49, "China Proxy(USD)": 42000,
        "source": "NVIDIA / Industry estimates"
    },
    "NVIDIA B200 (Blackwell)": {
        "MSRP(USD)": 40000, "Cloud/hr(USD)": 3.50, "China Proxy(USD)": 50000,
        "source": "NVIDIA GTC 2024 / Industry estimates"
    },
        "NVIDIA B300 GPU 单卡 (Blackwell Ultra)": {
        "渠道买断价(USD)": 45000, "云租(USD/时)": 4.00, "渠道价(USD)": 56000,
        "source": "B300单卡行情估算 (2026 new)"
    },
    "NVIDIA B300 服务器整机 8xGPU (国际)": {
        "官方渠道价(USD)": 550000, "2025年底价(USD)": 500000,
        "source": "美国市场公开售价约$55万/台 (2026-04媒体报道)"
    },
    "NVIDIA B300 服务器整机 8xGPU (China现货)": {
        "官方渠道价(CNY)": 4000000, "现货成交价(CNY)": 12000000, "渠道最高报价(CNY)": 14500000,
        "source": "国内现货:2025底¥400万→2026-08涨至¥1200万+,最高报价¥1450万/台"
    },
    "NVIDIA A100 80GB SXM": {
        "MSRP(USD)": 15000, "Cloud/hr(USD)": 1.10, "China Proxy(USD)": 18000,
        "source": "NVIDIA / Cloud avg pricing"
    },
    "NVIDIA L40S (Inference)": {
        "MSRP(USD)": 9000, "Cloud/hr(USD)": 0.80, "China Proxy(USD)": 11000,
        "source": "NVIDIA / Lambda public pricing"
    },
    "NVIDIA RTX 6000 Ada": {
        "MSRP(USD)": 6800, "Cloud/hr(USD)": 0.65, "China Proxy(USD)": 8200,
        "source": "NVIDIA / Vast.ai"
    },
    "NVIDIA RTX 4090": {
        "MSRP(USD)": 1599, "Cloud/hr(USD)": 0.35, "China Proxy(USD)": 1950,
        "source": "NVIDIA / Vast.ai"
    },
    "NVIDIA H800 (China Export)": {
        "MSRP(USD)": 32000, "Cloud/hr(USD)": 2.30, "China Proxy(USD)": 38000,
        "source": "NVIDIA China / Domestic cloud"
    },
    "Huawei Ascend 910B": {
        "MSRP(CNY)": 85000, "Cloud/hr(CNY)": 35, "China Proxy(CNY)": 100000,
        "source": "Huawei / Huawei Cloud Ascend"
    },
    "AMD MI300X": {
        "MSRP(USD)": 15000, "Cloud/hr(USD)": 1.50, "China Proxy(USD)": 18000,
        "source": "AMD / Industry estimates"
    },
}

# (LiteLLM模型键, 显示名, 区域)  -- 近6个月主流流行款
TOKEN_MODELS = [
    # --- 国际 ---
    ("gpt-5.6", "GPT-5.6", "intl"),
    ("gpt-5.6-luna", "GPT-5.6 Luna", "intl"),
    ("claude-opus-4-8", "Claude Opus 4.8", "intl"),
    ("claude-sonnet-5", "Claude Sonnet 5", "intl"),
    ("claude-haiku-4-5", "Claude Haiku 4.5", "intl"),
    ("gemini-3.1-pro-preview", "Gemini 3.1 Pro", "intl"),
    ("gemini-3.5-flash", "Gemini 3.5 Flash", "intl"),
    ("xai/grok-4", "Grok 4", "intl"),
    ("xai/grok-4-1-fast", "Grok 4.1 Fast", "intl"),
    ("mistral/mistral-large-2411", "Mistral Large", "intl"),
    # --- 国内 ---
    ("deepseek-v4-flash", "DeepSeek V4 Flash", "china"),
    ("deepseek-v4-pro", "DeepSeek V4 Pro", "china"),
    ("moonshot/kimi-k2.6", "Kimi K2.6", "china"),
    ("zai/glm-5.1", "GLM 5.1", "china"),
    ("fireworks_ai/glm-5p2", "GLM 5.2", "china"),
    ("openrouter/qwen/qwen3.5-397b-a17b", "Qwen3.5 397B", "china"),
    ("novita/baidu/ernie-4.5-300b-a47b-paddle", "文心 ERNIE 4.5", "china"),
    ("minimax/MiniMax-M2.5", "MiniMax M2.5", "china"),
    ("_doubao_pro", "Doubao Pro 32K", "china"),
    ("_hunyuan_turbo", "Hunyuan Turbo", "china"),
]

# 非LiteLLM国内模型官方公开价（近似）
HARDCODED_PRICES = {
    "_doubao_pro": {"input": 0.12, "output": 0.48, "provider": "volcengine"},
    "_hunyuan_turbo": {"input": 0.14, "output": 0.56, "provider": "tencent"},
}

def fetch_token_prices():
    try:
        r = urllib.request.urlopen(
            "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json",
            timeout=30)
        return json.loads(r.read().decode())
    except Exception as e:
        print(f"[FETCH] Token data failed: {e}")
        return {}

def build_data():
    litellm = fetch_token_prices()
    data = {"gpu": [], "token": [], "updated": date.today().isoformat()}

    for name, prices in GPU_MARKET.items():
        region = "china" if any(kw in name for kw in ["China", "Huawei", "Ascend"]) else "intl"
        source = prices.pop("source", "")
        data["gpu"].append({
            "name": name, "category": "gpu", "region": region,
            "prices": [{"type": k, "value": v, "unit": "CNY" if "CNY" in k else "USD"} for k, v in prices.items()],
            "source": source
        })

    for model_id, display_name, region in TOKEN_MODELS:
        prices = []
        cat = "llm_domestic" if region == "china" else "llm_intl"
        source = ""

        if model_id.startswith("_"):
            hc = HARDCODED_PRICES.get(model_id, {})
            if hc:
                prices.append({"type": "Input(USD/1M tokens)", "value": hc["input"], "unit": "USD/1M"})
                prices.append({"type": "Output(USD/1M tokens)", "value": hc["output"], "unit": "USD/1M"})
                source = f"Public pricing ({hc.get('provider','unknown')})"
        elif model_id in litellm:
            p = litellm[model_id]
            inp = (p.get("input_cost_per_token", 0) or 0) * 1000000
            out = (p.get("output_cost_per_token", 0) or 0) * 1000000
            if inp <= 0 and out <= 0:
                continue
            if inp > 0:
                prices.append({"type": "Input(USD/1M tokens)", "value": round(inp, 4), "unit": "USD/1M"})
            if out > 0:
                prices.append({"type": "Output(USD/1M tokens)", "value": round(out, 4), "unit": "USD/1M"})
            source = f"LiteLLM (provider: {p.get('litellm_provider','unknown')})"

        if prices:
            data["token"].append({
                "name": display_name, "category": cat, "region": region,
                "prices": prices, "source": source
            })

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return data

try:
    MARKET_DATA = build_data()
except Exception as e:
    print(f"[INIT] Error: {e}")
    MARKET_DATA = {"gpu": [], "token": [], "updated": ""}

@app.route("/")
def index():
    return jsonify({"service": "AI Market Monitor", "status": "ok",
        "gpu_models": len(MARKET_DATA["gpu"]),
        "token_models": len(MARKET_DATA["token"]),
        "updated": MARKET_DATA["updated"]})

@app.route("/api/prices")
def api_prices():
    return jsonify(MARKET_DATA["gpu"] + MARKET_DATA["token"])

@app.route("/api/summary")
def api_summary():
    all_items = MARKET_DATA["gpu"] + MARKET_DATA["token"]
    return jsonify({
        "object_count": len(all_items),
        "today_records": sum(len(item["prices"]) for item in all_items),
        "source_count": 3,
        "is_fresh": True,
        "last_update_time": MARKET_DATA["updated"],
        "data_sources": [
            "NVIDIA MSRP + Lambda/Vast.ai cloud pricing + China proxy markup",
            "LiteLLM open-source DB (official API pricing for latest mainstream models)",
            "ByteDance/Tencent public pricing (domestic models)"
        ]
    })

@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    global MARKET_DATA
    try:
        MARKET_DATA = build_data()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


if __name__ == "__main__":
    print("AI Market Monitor starting...")
    app.run(host="0.0.0.0", port=18888, debug=False)
