# -*- coding: utf-8 -*-
"""AI行情趋势监控 - 数据库模型与种子数据"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
import random

from config import DATABASE_PATH, DATA_DIR

os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = DATABASE_PATH


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS monitor_objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            unit TEXT DEFAULT '',
            region TEXT DEFAULT '国际',
            description TEXT DEFAULT '',
            source_urls TEXT DEFAULT '[]',
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS price_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            object_id INTEGER NOT NULL,
            price_type TEXT NOT NULL,
            price_value REAL NOT NULL,
            price_unit TEXT DEFAULT '',
            source_name TEXT DEFAULT '',
            record_date TEXT NOT NULL,
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (object_id) REFERENCES monitor_objects(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS update_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_type TEXT NOT NULL,
            status TEXT DEFAULT 'success',
            message TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE INDEX IF NOT EXISTS idx_price_obj_date ON price_records(object_id, record_date);
        CREATE INDEX IF NOT EXISTS idx_price_type ON price_records(price_type);
    ''')
    conn.commit()
    conn.close()


def seed_data():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM monitor_objects")
    count = c.fetchone()[0]
    if count > 0:
        conn.close()
        return

    objects = [
        # === GPU 硬件 ===
        {"name": "NVIDIA H100 80GB PCIe", "category": "gpu", "subcategory": "GPU显卡", "unit": "美元/张", "region": "国际", "sort": 1},
        {"name": "NVIDIA H100 80GB SXM", "category": "gpu", "subcategory": "GPU显卡", "unit": "美元/张", "region": "国际", "sort": 2},
        {"name": "NVIDIA H200 141GB", "category": "gpu", "subcategory": "GPU显卡", "unit": "美元/张", "region": "国际", "sort": 3},
        {"name": "NVIDIA B300 服务器", "category": "gpu", "subcategory": "GPU服务器", "unit": "美元/台", "region": "国际", "sort": 4},
        {"name": "NVIDIA H100 80GB PCIe (国内)", "category": "gpu", "subcategory": "GPU显卡", "unit": "万元/张", "region": "国内", "sort": 5},
        {"name": "NVIDIA H100 80GB SXM (国内)", "category": "gpu", "subcategory": "GPU显卡", "unit": "万元/张", "region": "国内", "sort": 6},
        {"name": "NVIDIA H200 141GB (国内)", "category": "gpu", "subcategory": "GPU显卡", "unit": "万元/张", "region": "国内", "sort": 7},
        {"name": "NVIDIA B300 服务器 (国内)", "category": "gpu", "subcategory": "GPU服务器", "unit": "万元/台", "region": "国内", "sort": 8},

        # === 国际大模型 Token ===
        {"name": "OpenAI GPT-4o", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 9},
        {"name": "OpenAI GPT-4o-mini", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 10},
        {"name": "OpenAI o4-mini", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 11},
        {"name": "Anthropic Claude 3.5 Sonnet", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 12},
        {"name": "Anthropic Claude 3 Opus", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 13},
        {"name": "Google Gemini 2.5 Pro", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 14},
        {"name": "Google Gemini 2.5 Flash", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 15},
        {"name": "xAI Grok-3", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 16},
        {"name": "Meta Llama 4 (Together AI)", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 17},
        {"name": "Mistral Large 2", "category": "llm_intl", "subcategory": "国际大模型", "unit": "美元/百万Token", "region": "国际", "sort": 18},

        # === 国内大模型 Token ===
        {"name": "DeepSeek-V3", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 19},
        {"name": "DeepSeek-R1", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 20},
        {"name": "阿里通义千问 Qwen3-Plus", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 21},
        {"name": "阿里通义千问 Qwen3-Max", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 22},
        {"name": "百度文心一言 4.0 Turbo", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 23},
        {"name": "字节豆包 Pro", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 24},
        {"name": "智谱 GLM-4 Plus", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 25},
        {"name": "月之暗面 Kimi", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 26},
        {"name": "讯飞星火 4.0", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 27},
        {"name": "MiniMax abab7", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 28},
        {"name": "零一万物 Yi-Large", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 29},
        {"name": "百川 Baichuan 4", "category": "llm_domestic", "subcategory": "国内大模型", "unit": "元/百万Token", "region": "国内", "sort": 30},
    ]

    for obj in objects:
        c.execute('''INSERT INTO monitor_objects (name, category, subcategory, unit, region, sort_order)
                     VALUES (?,?,?,?,?,?)''',
                  (obj["name"], obj["category"], obj["subcategory"], obj["unit"], obj["region"], obj["sort"]))

    conn.commit()

    # 生成种子价格数据
    seed_prices = get_seed_prices()
    obj_ids = {r["name"]: r["id"] for r in c.execute("SELECT id, name FROM monitor_objects").fetchall()}

    today = datetime.now()
    for days_ago in range(365):
        date_str = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        for name, price_types in seed_prices.items():
            obj_id = obj_ids.get(name)
            if not obj_id:
                continue
            for ptype, base_price_info in price_types.items():
                base = base_price_info["base"]
                vol = base_price_info.get("vol", base * 0.05)
                trend = base_price_info.get("trend", 0)
                trend_effect = trend * days_ago / 365.0
                noise = random.gauss(0, vol)
                price = max(base * 0.5, base + trend_effect + noise)
                price = round(price, 2)
                c.execute('''INSERT INTO price_records (object_id, price_type, price_value, price_unit, record_date)
                             VALUES (?,?,?,?,?)''',
                          (obj_id, ptype, price, base_price_info["unit"], date_str))

    conn.commit()
    conn.close()


def get_seed_prices():
    return {
        # GPU 硬件 - 国际价格 ($)
        "NVIDIA H100 80GB PCIe": {
            "官方价": {"base": 28000, "vol": 500, "trend": -3000, "unit": "USD"},
            "代理价": {"base": 31000, "vol": 600, "trend": -2500, "unit": "USD"},
            "云平台时租": {"base": 3.50, "vol": 0.30, "trend": -0.40, "unit": "USD/h"},
        },
        "NVIDIA H100 80GB SXM": {
            "官方价": {"base": 33000, "vol": 500, "trend": -3500, "unit": "USD"},
            "代理价": {"base": 36000, "vol": 600, "trend": -3000, "unit": "USD"},
            "云平台时租": {"base": 4.20, "vol": 0.30, "trend": -0.50, "unit": "USD/h"},
        },
        "NVIDIA H200 141GB": {
            "官方价": {"base": 40000, "vol": 800, "trend": -2000, "unit": "USD"},
            "代理价": {"base": 45000, "vol": 1000, "trend": -1500, "unit": "USD"},
            "云平台时租": {"base": 5.50, "vol": 0.40, "trend": -0.30, "unit": "USD/h"},
        },
        "NVIDIA B300 服务器": {
            "官方价": {"base": 450000, "vol": 10000, "trend": -10000, "unit": "USD"},
            "代理价": {"base": 500000, "vol": 12000, "trend": -8000, "unit": "USD"},
            "云平台月租": {"base": 25000, "vol": 1500, "trend": -500, "unit": "USD/月"},
        },
        # GPU 硬件 - 国内价格 (万元)
        "NVIDIA H100 80GB PCIe (国内)": {
            "官方价": {"base": 22.0, "vol": 1.0, "trend": -3.0, "unit": "万元"},
            "代理价": {"base": 25.0, "vol": 1.2, "trend": -2.5, "unit": "万元"},
            "第三方平台价": {"base": 24.0, "vol": 1.5, "trend": -2.0, "unit": "万元"},
        },
        "NVIDIA H100 80GB SXM (国内)": {
            "官方价": {"base": 26.0, "vol": 1.0, "trend": -3.5, "unit": "万元"},
            "代理价": {"base": 29.0, "vol": 1.2, "trend": -3.0, "unit": "万元"},
            "第三方平台价": {"base": 28.0, "vol": 1.5, "trend": -2.5, "unit": "万元"},
        },
        "NVIDIA H200 141GB (国内)": {
            "官方价": {"base": 32.0, "vol": 1.5, "trend": -2.0, "unit": "万元"},
            "代理价": {"base": 36.0, "vol": 2.0, "trend": -1.5, "unit": "万元"},
            "第三方平台价": {"base": 34.0, "vol": 2.0, "trend": -1.0, "unit": "万元"},
        },
        "NVIDIA B300 服务器 (国内)": {
            "官方价": {"base": 350.0, "vol": 15, "trend": -10, "unit": "万元"},
            "代理价": {"base": 400.0, "vol": 20, "trend": -8, "unit": "万元"},
            "第三方平台价": {"base": 380.0, "vol": 18, "trend": -5, "unit": "万元"},
        },
        # 国际大模型 Token 价格 (USD/百万Token)
        "OpenAI GPT-4o": {
            "官方价(Input)": {"base": 2.50, "vol": 0.15, "trend": -0.30, "unit": "USD/1M"},
            "官方价(Output)": {"base": 10.00, "vol": 0.50, "trend": -1.20, "unit": "USD/1M"},
            "代理价(Input)": {"base": 3.00, "vol": 0.20, "trend": -0.30, "unit": "USD/1M"},
            "代理价(Output)": {"base": 12.00, "vol": 0.60, "trend": -1.00, "unit": "USD/1M"},
        },
        "OpenAI GPT-4o-mini": {
            "官方价(Input)": {"base": 0.15, "vol": 0.02, "trend": -0.02, "unit": "USD/1M"},
            "官方价(Output)": {"base": 0.60, "vol": 0.05, "trend": -0.08, "unit": "USD/1M"},
        },
        "OpenAI o4-mini": {
            "官方价(Input)": {"base": 1.10, "vol": 0.08, "trend": -0.15, "unit": "USD/1M"},
            "官方价(Output)": {"base": 4.40, "vol": 0.25, "trend": -0.50, "unit": "USD/1M"},
        },
        "Anthropic Claude 3.5 Sonnet": {
            "官方价(Input)": {"base": 3.00, "vol": 0.15, "trend": -0.20, "unit": "USD/1M"},
            "官方价(Output)": {"base": 15.00, "vol": 0.80, "trend": -1.00, "unit": "USD/1M"},
        },
        "Anthropic Claude 3 Opus": {
            "官方价(Input)": {"base": 15.00, "vol": 0.50, "trend": -2.00, "unit": "USD/1M"},
            "官方价(Output)": {"base": 75.00, "vol": 3.00, "trend": -8.00, "unit": "USD/1M"},
        },
        "Google Gemini 2.5 Pro": {
            "官方价(Input)": {"base": 1.25, "vol": 0.10, "trend": -0.15, "unit": "USD/1M"},
            "官方价(Output)": {"base": 10.00, "vol": 0.50, "trend": -0.80, "unit": "USD/1M"},
        },
        "Google Gemini 2.5 Flash": {
            "官方价(Input)": {"base": 0.15, "vol": 0.02, "trend": -0.02, "unit": "USD/1M"},
            "官方价(Output)": {"base": 0.60, "vol": 0.05, "trend": -0.06, "unit": "USD/1M"},
        },
        "xAI Grok-3": {
            "官方价(Input)": {"base": 5.00, "vol": 0.30, "trend": -0.50, "unit": "USD/1M"},
            "官方价(Output)": {"base": 15.00, "vol": 0.80, "trend": -1.50, "unit": "USD/1M"},
        },
        "Meta Llama 4 (Together AI)": {
            "平台价(Input)": {"base": 0.20, "vol": 0.02, "trend": 0.00, "unit": "USD/1M"},
            "平台价(Output)": {"base": 0.80, "vol": 0.05, "trend": -0.05, "unit": "USD/1M"},
        },
        "Mistral Large 2": {
            "官方价(Input)": {"base": 2.00, "vol": 0.15, "trend": -0.20, "unit": "USD/1M"},
            "官方价(Output)": {"base": 6.00, "vol": 0.30, "trend": -0.50, "unit": "USD/1M"},
        },
        # 国内大模型 Token 价格 (元/百万Token)
        "DeepSeek-V3": {
            "官方价(Input)": {"base": 1.00, "vol": 0.10, "trend": -0.10, "unit": "元/1M"},
            "官方价(Output)": {"base": 2.00, "vol": 0.15, "trend": -0.20, "unit": "元/1M"},
        },
        "DeepSeek-R1": {
            "官方价(Input)": {"base": 4.00, "vol": 0.30, "trend": -0.50, "unit": "元/1M"},
            "官方价(Output)": {"base": 16.00, "vol": 1.00, "trend": -2.00, "unit": "元/1M"},
        },
        "阿里通义千问 Qwen3-Plus": {
            "官方价(Input)": {"base": 0.80, "vol": 0.08, "trend": -0.08, "unit": "元/1M"},
            "官方价(Output)": {"base": 2.00, "vol": 0.15, "trend": -0.20, "unit": "元/1M"},
        },
        "阿里通义千问 Qwen3-Max": {
            "官方价(Input)": {"base": 0.50, "vol": 0.05, "trend": -0.05, "unit": "元/1M"},
            "官方价(Output)": {"base": 2.00, "vol": 0.15, "trend": -0.20, "unit": "元/1M"},
        },
        "百度文心一言 4.0 Turbo": {
            "官方价(Input)": {"base": 30.00, "vol": 2.00, "trend": -5.00, "unit": "元/1M"},
            "官方价(Output)": {"base": 100.00, "vol": 5.00, "trend": -10.00, "unit": "元/1M"},
        },
        "字节豆包 Pro": {
            "官方价(Input)": {"base": 0.80, "vol": 0.08, "trend": -0.10, "unit": "元/1M"},
            "官方价(Output)": {"base": 2.00, "vol": 0.15, "trend": -0.20, "unit": "元/1M"},
        },
        "智谱 GLM-4 Plus": {
            "官方价(Input)": {"base": 50.00, "vol": 3.00, "trend": -8.00, "unit": "元/1M"},
            "官方价(Output)": {"base": 100.00, "vol": 5.00, "trend": -10.00, "unit": "元/1M"},
        },
        "月之暗面 Kimi": {
            "官方价(Input)": {"base": 12.00, "vol": 1.00, "trend": -2.00, "unit": "元/1M"},
            "官方价(Output)": {"base": 60.00, "vol": 3.00, "trend": -8.00, "unit": "元/1M"},
        },
        "讯飞星火 4.0": {
            "官方价(Input)": {"base": 30.00, "vol": 2.00, "trend": -5.00, "unit": "元/1M"},
            "官方价(Output)": {"base": 100.00, "vol": 5.00, "trend": -10.00, "unit": "元/1M"},
        },
        "MiniMax abab7": {
            "官方价(Input)": {"base": 0.50, "vol": 0.05, "trend": -0.05, "unit": "元/1M"},
            "官方价(Output)": {"base": 1.00, "vol": 0.10, "trend": -0.10, "unit": "元/1M"},
        },
        "零一万物 Yi-Large": {
            "官方价(Input)": {"base": 10.00, "vol": 0.80, "trend": -1.50, "unit": "元/1M"},
            "官方价(Output)": {"base": 30.00, "vol": 2.00, "trend": -4.00, "unit": "元/1M"},
        },
        "百川 Baichuan 4": {
            "官方价(Input)": {"base": 20.00, "vol": 1.50, "trend": -3.00, "unit": "元/1M"},
            "官方价(Output)": {"base": 60.00, "vol": 3.00, "trend": -6.00, "unit": "元/1M"},
        },
    }