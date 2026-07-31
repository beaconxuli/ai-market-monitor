# -*- coding: utf-8 -*-
"""AI行情趋势监控 - 数据采集模块"""

import json
import random
import time
from datetime import datetime, timedelta
import sqlite3

from models import get_db, seed_data


def check_data_freshness():
    """检查数据是否在24小时内更新过，返回True表示数据新鲜"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT MAX(created_at) FROM price_records")
    last = c.fetchone()[0]
    conn.close()
    if not last:
        return False
    last_dt = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
    return (datetime.now() - last_dt).total_seconds() < 24 * 3600


def get_today_records():
    """获取今日价格记录，如果没有则生成"""
    conn = get_db()
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM price_records WHERE record_date = ?", (today,))
    count = c.fetchone()[0]
    conn.close()

    if count == 0:
        generate_today_records()


def generate_today_records():
    """基于前一天价格生成今日价格（模拟数据采集）"""
    conn = get_db()
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    c.execute("SELECT id, name, category FROM monitor_objects WHERE is_active = 1")
    objects = c.fetchall()

    for obj in objects:
        c.execute('''SELECT price_type, price_value, price_unit, source_name
                     FROM price_records
                     WHERE object_id = ? AND record_date = ?
                     ORDER BY price_type''', (obj["id"], yesterday))
        yesterday_records = c.fetchall()

        if not yesterday_records:
            continue

        for rec in yesterday_records:
            vol_pct = 0.02
            noise = random.gauss(0, rec["price_value"] * vol_pct)
            new_price = round(max(0.01, rec["price_value"] + noise), 2)
            c.execute('''INSERT INTO price_records (object_id, price_type, price_value, price_unit, record_date, source_name)
                         VALUES (?,?,?,?,?,?)''',
                      (obj["id"], rec["price_type"], new_price, rec["price_unit"], today, rec["source_name"]))

    # 记录更新日志
    c.execute('''INSERT INTO update_log (update_type, status, message)
                 VALUES ('daily_update', 'success', ?)''',
              (f"已生成 {today} 的日度价格数据，共 {len(objects)} 个监控对象",))
    conn.commit()
    conn.close()


def fetch_latest_prices(object_id=None):
    """获取最新价格数据"""
    conn = get_db()
    c = conn.cursor()

    if object_id:
        c.execute('''SELECT m.id, m.name, m.category, m.unit, m.region,
                            pr.price_type, pr.price_value, pr.price_unit, pr.record_date, pr.source_name
                     FROM monitor_objects m
                     LEFT JOIN price_records pr ON m.id = pr.object_id
                     WHERE m.id = ? AND m.is_active = 1
                     AND pr.record_date = (SELECT MAX(record_date) FROM price_records WHERE object_id = m.id)
                     ORDER BY pr.price_type''', (object_id,))
    else:
        c.execute('''SELECT m.id, m.name, m.category, m.unit, m.region,
                            pr.price_type, pr.price_value, pr.price_unit, pr.record_date, pr.source_name
                     FROM monitor_objects m
                     LEFT JOIN price_records pr ON m.id = pr.object_id
                     WHERE m.is_active = 1
                     AND pr.record_date = (SELECT MAX(record_date) FROM price_records WHERE object_id = m.id)
                     ORDER BY m.sort_order, pr.price_type''')

    rows = c.fetchall()
    conn.close()

    result = {}
    for row in rows:
        oid = row["id"]
        if oid not in result:
            result[oid] = {
                "id": oid,
                "name": row["name"],
                "category": row["category"],
                "unit": row["unit"],
                "region": row["region"],
                "record_date": row["record_date"],
                "prices": []
            }
        if row["price_type"]:
            result[oid]["prices"].append({
                "price_type": row["price_type"],
                "price_value": row["price_value"],
                "price_unit": row["price_unit"],
                "source_name": row["source_name"]
            })

    return list(result.values())


def get_price_trend(object_id, days=30):
    """获取指定对象的价格趋势数据"""
    conn = get_db()
    c = conn.cursor()
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    c.execute('''SELECT price_type, price_value, record_date
                 FROM price_records
                 WHERE object_id = ? AND record_date >= ?
                 ORDER BY record_date, price_type''', (object_id, start_date))
    rows = c.fetchall()
    conn.close()

    trends = {}
    for row in rows:
        ptype = row["price_type"]
        if ptype not in trends:
            trends[ptype] = []
        trends[ptype].append({
            "date": row["record_date"],
            "value": row["price_value"]
        })

    return trends


def get_monitor_objects(category=None):
    """获取所有监控对象"""
    conn = get_db()
    c = conn.cursor()
    if category:
        c.execute('''SELECT * FROM monitor_objects WHERE is_active = 1 AND category = ?
                     ORDER BY sort_order''', (category,))
    else:
        c.execute('''SELECT * FROM monitor_objects WHERE is_active = 1
                     ORDER BY sort_order''')

    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_monitor_object(name, category, subcategory, unit, region, description=""):
    """手动添加监控对象"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO monitor_objects (name, category, subcategory, unit, region, description, sort_order)
                 VALUES (?,?,?,?,?,?,
                 (SELECT COALESCE(MAX(sort_order),0)+1 FROM monitor_objects))''',
              (name, category, subcategory, unit, region, description))
    oid = c.lastrowid

    # 生成过去365天种子数据
    today = datetime.now()
    base_price = 1.0
    for days_ago in range(365):
        date_str = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        noise = random.gauss(0, base_price * 0.05)
        price = round(max(0.01, base_price + noise), 2)
        c.execute('''INSERT INTO price_records (object_id, price_type, price_value, price_unit, record_date)
                     VALUES (?,?,?,?,?)''',
                  (oid, "参考价", price, unit, date_str))

    conn.commit()
    conn.close()
    return oid


def update_monitor_object(obj_id, **kwargs):
    """更新监控对象"""
    conn = get_db()
    c = conn.cursor()
    allowed = ["name", "category", "subcategory", "unit", "region", "description", "is_active"]
    updates = {k: v for k, v in kwargs.items() if k in allowed}
    if updates:
        updates["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_clause = ", ".join(f"{k}=?" for k in updates)
        c.execute(f"UPDATE monitor_objects SET {set_clause} WHERE id=?", (*updates.values(), obj_id))
        conn.commit()
    conn.close()


def update_single_price(obj_id, price_type, price_value, source_name=""):
    """手动更新单条价格"""
    conn = get_db()
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute('''INSERT OR REPLACE INTO price_records (object_id, price_type, price_value, record_date, source_name)
                 VALUES (?,?,?,?,?)''', (obj_id, price_type, price_value, today, source_name))
    conn.commit()
    conn.close()


def get_update_logs(limit=20):
    """获取更新日志"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM update_log ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_summary_stats():
    """获取首页摘要统计"""
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM monitor_objects WHERE is_active=1")
    total_objects = c.fetchone()[0]

    c.execute("SELECT MAX(record_date) FROM price_records")
    last_update = c.fetchone()[0] or "暂无"

    c.execute("SELECT MAX(created_at) FROM update_log WHERE update_type='daily_update'")
    last_daily = c.fetchone()[0] or "暂无"

    # 今日价格记录数
    from datetime import date
    today_str = date.today().isoformat()
    c.execute("SELECT COUNT(*) FROM price_records WHERE record_date=?", (today_str,))
    today_records = c.fetchone()[0]

    # 数据来源数
    from config import DATA_SOURCES
    source_count = sum(
        sum(len(links) for links in regions.values())
        for regions in DATA_SOURCES.values()
    )

    conn.close()
    return {
        "total_objects": total_objects,
        "object_count": total_objects,
        "today_records": today_records,
        "source_count": source_count,
        "last_data_date": last_update,
        "last_update_time": last_daily,
        "is_fresh": check_data_freshness()
    }
