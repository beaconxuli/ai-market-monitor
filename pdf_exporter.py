# -*- coding: utf-8 -*-
"""AI行情趋势监控 - PDF报告导出模块"""

import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import REPORT_DIR, BASE_DIR
from data_fetcher import fetch_latest_prices, get_summary_stats

_FONT_NAME = "Helvetica"
_FONT_NAME_BOLD = "Helvetica-Bold"

def _register_fonts():
    global _FONT_NAME, _FONT_NAME_BOLD
    font_candidates = [
        ("C:/Windows/Fonts/msyh.ttc", "MSYH"),
        ("C:/Windows/Fonts/simsun.ttc", "SIMSUN"),
        ("C:/Windows/Fonts/simhei.ttf", "SIMHEI"),
    ]
    for fpath, fname in font_candidates:
        if os.path.exists(fpath):
            try:
                pdfmetrics.registerFont(TTFont(fname, fpath))
                _FONT_NAME = fname
                _FONT_NAME_BOLD = fname
                return
            except Exception:
                continue


def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'CNTitle', fontName=_FONT_NAME_BOLD, fontSize=20, leading=28,
        alignment=TA_CENTER, spaceAfter=16, textColor=HexColor("#1a1a2e")
    ))
    styles.add(ParagraphStyle(
        'CNH1', fontName=_FONT_NAME_BOLD, fontSize=14, leading=20,
        spaceBefore=16, spaceAfter=8, textColor=HexColor("#16213e")
    ))
    styles.add(ParagraphStyle(
        'CNH2', fontName=_FONT_NAME_BOLD, fontSize=11, leading=16,
        spaceBefore=10, spaceAfter=6, textColor=HexColor("#0f3460")
    ))
    styles.add(ParagraphStyle(
        'CNBody', fontName=_FONT_NAME, fontSize=9, leading=14,
        spaceAfter=5, textColor=HexColor("#333333")
    ))
    styles.add(ParagraphStyle(
        'CNSmall', fontName=_FONT_NAME, fontSize=7, leading=10,
        textColor=HexColor("#888888")
    ))
    styles.add(ParagraphStyle(
        'CNTableHeader', fontName=_FONT_NAME_BOLD, fontSize=8, leading=12,
        textColor=white, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'CNTableCell', fontName=_FONT_NAME, fontSize=7, leading=10,
        textColor=HexColor("#333333"), alignment=TA_CENTER
    ))
    return styles


def build_price_table(objects_data, styles):
    header = [
        Paragraph("Monitor Object", styles["CNTableHeader"]),
        Paragraph("Category", styles["CNTableHeader"]),
        Paragraph("Region", styles["CNTableHeader"]),
        Paragraph("Price Type", styles["CNTableHeader"]),
        Paragraph("Latest Price", styles["CNTableHeader"]),
        Paragraph("Unit", styles["CNTableHeader"]),
    ]
    data = [header]
    for obj in objects_data:
        for price in obj["prices"]:
            data.append([
                Paragraph(obj["name"][:40], styles["CNTableCell"]),
                Paragraph(obj["category"][:15], styles["CNTableCell"]),
                Paragraph(obj["region"][:10], styles["CNTableCell"]),
                Paragraph(price["price_type"][:20], styles["CNTableCell"]),
                Paragraph(f"{price['price_value']:.2f}", styles["CNTableCell"]),
                Paragraph(price.get("price_unit", "")[:15], styles["CNTableCell"]),
            ])
    col_widths = [110, 60, 35, 70, 60, 55]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor("#f5f5f5")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return table


def export_pdf_report(report_type="full"):
    _register_fonts()
    styles = get_styles()
    os.makedirs(REPORT_DIR, exist_ok=True)

    now = datetime.now()
    filename = f"AI_Market_Report_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(REPORT_DIR, filename)

    doc = SimpleDocTemplate(
        filepath, pagesize=A4,
        rightMargin=15*mm, leftMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm,
        title="AI Infrastructure & Token Market Report"
    )

    story = []

    # Cover
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("AI Infrastructure & Token", styles["CNTitle"]))
    story.append(Paragraph("Market Analysis Report", styles["CNTitle"]))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(f"Report Date: {now.strftime('%Y-%m-%d')}", styles["CNBody"]))
    story.append(Paragraph(f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}", styles["CNBody"]))
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#1a1a2e")))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Coverage:", styles["CNBody"]))
    story.append(Paragraph("  - NVIDIA GPU Hardware (H100/H200/B300)", styles["CNBody"]))
    story.append(Paragraph("  - International LLM Token Pricing (OpenAI/Anthropic/Google/xAI/Meta/Mistral)", styles["CNBody"]))
    story.append(Paragraph("  - Domestic LLM Token Pricing (DeepSeek/Qwen/ERNIE/Doubao/Kimi/Spark/GLM/MiniMax/Yi/Baichuan)", styles["CNBody"]))
    story.append(PageBreak())

    # Summary
    stats = get_summary_stats()
    story.append(Paragraph("I. Executive Summary", styles["CNH1"]))
    story.append(Paragraph(f"Monitored Objects: {stats['total_objects']}", styles["CNBody"]))
    story.append(Paragraph(f"Latest Data Date: {stats['last_data_date']}", styles["CNBody"]))
    story.append(Paragraph(f"Last Update: {stats['last_update_time']}", styles["CNBody"]))
    story.append(Paragraph(f"Data Freshness: {'Within 24h' if stats['is_fresh'] else 'Needs Update'}", styles["CNBody"]))
    story.append(Spacer(1, 5*mm))

    # GPU Hardware
    all_prices = fetch_latest_prices()
    gpu_data = [o for o in all_prices if o["category"] == "gpu"]
    intl_llm = [o for o in all_prices if o["category"] == "llm_intl"]
    domestic_llm = [o for o in all_prices if o["category"] == "llm_domestic"]

    story.append(Paragraph("II. GPU Hardware Pricing", styles["CNH1"]))
    if gpu_data:
        story.append(build_price_table(gpu_data, styles))
    story.append(Spacer(1, 5*mm))

    # International LLM
    story.append(PageBreak())
    story.append(Paragraph("III. International LLM Token Pricing", styles["CNH1"]))
    if intl_llm:
        story.append(build_price_table(intl_llm, styles))
    story.append(Spacer(1, 5*mm))

    # Domestic LLM
    story.append(PageBreak())
    story.append(Paragraph("IV. Domestic LLM Token Pricing", styles["CNH1"]))
    if domestic_llm:
        story.append(build_price_table(domestic_llm, styles))
    story.append(Spacer(1, 5*mm))

    # Analysis
    story.append(PageBreak())
    story.append(Paragraph("V. Market Analysis", styles["CNH1"]))

    story.append(Paragraph("1. GPU Hardware Market Trends", styles["CNH2"]))
    story.append(Paragraph(
        "NVIDIA H100/H200 series GPUs have shown a consistent downward price trend over the past year, "
        "driven by improving supply-demand dynamics and the upcoming B300 next-gen product ramp. "
        "H100 PCIe has declined from ~$35,000 to the $25,000-$28,000 range. B300 servers are priced "
        "at $400,000-$500,000 range and are expected to decline further in H2 2026 as production scales. "
        "China domestic market prices carry a 15-30% premium due to import/export restrictions.",
        styles["CNBody"]))

    story.append(Paragraph("2. International LLM Token Price Trends", styles["CNH2"]))
    story.append(Paragraph(
        "International LLM token pricing shows clear polarization: premium models (Claude 3 Opus, Grok-3) "
        "maintain high but declining prices; lightweight models (GPT-4o-mini, Gemini Flash) have dropped "
        "to extremely low levels ($0.15/M tokens), accelerating widespread AI adoption. "
        "The overall trend is 'premium down, budget to floor' as competition intensifies.",
        styles["CNBody"]))

    story.append(Paragraph("3. Domestic LLM Token Price Trends", styles["CNH2"]))
    story.append(Paragraph(
        "China's domestic LLM market has entered a 'price war' phase. DeepSeek has reshaped the market "
        "with ultra-low pricing (1-2 yuan/M tokens), forcing Alibaba Qwen, ByteDance Doubao to cut prices "
        "significantly. Traditional high-price models (Baidu ERNIE, iFlytek Spark) face severe competition. "
        "Third-party aggregation platforms further lower barriers to entry. Prices are expected to continue "
        "declining over the next 6 months.",
        styles["CNBody"]))

    story.append(Paragraph("4. Investment Implications", styles["CNH2"]))
    story.append(Paragraph(
        "(1) GPU Hardware: Monitor B300 production ramp; H100/H200 inventory clearance may create short-term "
        "price volatility. Compliant channels remain scarce in China.\n"
        "(2) Token Aggregation: Price war benefits aggregation platforms; 'low-cost models for traffic + "
        "value-added services for monetization' model worth watching.\n"
        "(3) Cross-border Compute: Hainan Free Trade Port policy advantages create arbitrage opportunities "
        "between low-cost domestic tokens and premium overseas markets.\n"
        "(4) Risk Factors: Regulatory changes, chip export controls escalation, open-source model disruption "
        "require continuous monitoring.",
        styles["CNBody"]))

    # Footer
    story.append(Spacer(1, 15*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=grey))
    story.append(Paragraph(
        f"Report generated by AI Market Monitor | {now.strftime('%Y-%m-%d %H:%M:%S')}",
        styles["CNSmall"])
    )
    story.append(Paragraph(
        "Data sources: Official vendor websites, cloud platform public pricing, third-party aggregators. "
        "For reference only, not investment advice.",
        styles["CNSmall"])
    )

    doc.build(story)
    return filepath