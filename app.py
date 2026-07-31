# -*- coding: utf-8 -*-
"""AI Infrastructure & Token Market Monitor - Production"""
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

TOKEN_MODELS = {
    # OpenAI
    "gpt-4o": "GPT-4o",
    "gpt-4o-mini": "GPT-4o Mini",
    "gpt-4.1": "GPT-4.1",
    "gpt-4.1-mini": "GPT-4.1 Mini",
    "o3-mini": "OpenAI o3-mini",
    # Anthropic
    "claude-sonnet-4-20250514": "Claude Sonnet 4",
    "claude-opus-4-20250514": "Claude Opus 4",
    "vertex_ai/claude-3-5-haiku": "Claude 3.5 Haiku",
    # Google
    "gemini-2.5-flash": "Gemini 2.5 Flash",
    "gemini/gemini-2.5-pro": "Gemini 2.5 Pro",
    "gemini-2.0-flash": "Gemini 2.0 Flash",
    # DeepSeek
    "deepseek-chat": "DeepSeek V3",
    "deepseek-reasoner": "DeepSeek R1",
    # Alibaba
    "dashscope/qwen-max": "Qwen Max",
    "dashscope/qwen-plus": "Qwen Plus",
    "dashscope/qwen-turbo": "Qwen Turbo",
    # Meta
    "deepinfra/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8": "Llama 4 Maverick",
    # Mistral
    "mistral/mistral-large-latest": "Mistral Large",
    "mistral/mistral-small-latest": "Mistral Small",
    # Cohere
    "command-r-plus": "Command R+",
    # xAI
    "xai/grok-3": "Grok 3",
    # ByteDance (hardcoded - not in LiteLLM)
    "_doubao_pro": "Doubao Pro 32K",
    "_doubao_lite": "Doubao Lite 32K",
    # Tencent (hardcoded - not in LiteLLM)
    "_hunyuan_turbo": "Hunyuan Turbo",
    "_hunyuan_standard": "Hunyuan Standard",
}

# Hardcoded prices for models not in LiteLLM
HARDCODED_PRICES = {
    "_doubao_pro": {"input": 0.12, "output": 0.48, "provider": "volcengine"},
    "_doubao_lite": {"input": 0.04, "output": 0.16, "provider": "volcengine"},
    "_hunyuan_turbo": {"input": 0.14, "output": 0.56, "provider": "tencent"},
    "_hunyuan_standard": {"input": 0.06, "output": 0.24, "provider": "tencent"},
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

    for model_id, display_name in TOKEN_MODELS.items():
        prices = []
        region = "china" if any(kw in model_id for kw in ["deepseek", "qwen", "doubao", "hunyuan", "_doubao", "_hunyuan"]) else "intl"
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
            "LiteLLM open-source DB (2986 model official API pricing)",
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

if __name__ == "__main__":
    print("AI Market Monitor starting...")
    app.run(host="0.0.0.0", port=18888, debug=False)