# -*- coding: utf-8 -*-
import os
"""AI行情趋势监控 - 配置文件"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

for d in [DATA_DIR, LOG_DIR, REPORT_DIR]:
    os.makedirs(d, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, "ai_market_monitor.db")
UPDATE_INTERVAL_HOURS = 24
MONITOR_REFRESH_DAYS = 30
FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.environ.get("FLASK_PORT", "18888"))
FLASK_DEBUG = False

DATA_SOURCES = {
    "GPU硬件": {
        "国际": [
            {"name": "NVIDIA官方", "url": "https://www.nvidia.com"},
            {"name": "Amazon AWS", "url": "https://aws.amazon.com/ec2/pricing/"},
            {"name": "Google Cloud", "url": "https://cloud.google.com/compute/gpus-pricing"},
            {"name": "Microsoft Azure", "url": "https://azure.microsoft.com/pricing/details/virtual-machines/"},
            {"name": "Lambda Labs", "url": "https://lambdalabs.com/service/gpu-cloud"},
            {"name": "RunPod", "url": "https://www.runpod.io/gpu-instance/pricing"},
        ],
        "国内": [
            {"name": "阿里云GPU", "url": "https://www.aliyun.com/product/ecs/gpu"},
            {"name": "腾讯云GPU", "url": "https://cloud.tencent.com/product/gpu"},
            {"name": "华为云GPU", "url": "https://www.huaweicloud.com/product/gpu.html"},
            {"name": "AutoDL算力云", "url": "https://www.autodl.com"},
            {"name": "恒源云", "url": "https://www.gpushare.com"},
        ]
    },
    "大模型Token": {
        "国际": [
            {"name": "OpenAI官方", "url": "https://openai.com/api/pricing/"},
            {"name": "Anthropic官方", "url": "https://www.anthropic.com/pricing"},
            {"name": "Google AI官方", "url": "https://ai.google.dev/pricing"},
            {"name": "Together AI", "url": "https://www.together.ai/pricing"},
            {"name": "Fireworks AI", "url": "https://fireworks.ai/pricing"},
            {"name": "Groq", "url": "https://groq.com/pricing/"},
        ],
        "国内": [
            {"name": "阿里云百炼", "url": "https://bailian.console.aliyun.com/"},
            {"name": "百度千帆", "url": "https://console.bce.baidu.com/qianfan/"},
            {"name": "腾讯混元", "url": "https://cloud.tencent.com/product/hunyuan"},
            {"name": "火山引擎(豆包)", "url": "https://www.volcengine.com/product/doubao"},
            {"name": "DeepSeek官方", "url": "https://platform.deepseek.com/api-docs/pricing"},
            {"name": "硅基流动", "url": "https://siliconflow.cn/pricing"},
            {"name": "智谱开放平台", "url": "https://open.bigmodel.cn/pricing"},
            {"name": "月之暗面开放平台", "url": "https://platform.moonshot.cn/pricing"},
        ]
    }
}