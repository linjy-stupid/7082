"""7082 项目全局配置。"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # F:\claude\7082\project
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
PROMPTS_DIR = ROOT / "prompts"

# SEC 要求 User-Agent 能识别到具体人。可用环境变量覆盖：
#   set SEC_UA=Your Name your@email.com
SEC_UA = os.environ.get("SEC_UA", "Jin Zhecheng u3036809385@connect.hku.hk")

TICKERS = ["NVDA", "MSFT", "PLTR"]

# CIK 来自 SEC 官方 company_tickers.json（000 前缀为 SEC 惯例的 10 位补零）
CIK = {
    "NVDA": "0001045810",
    "MSFT": "0000789019",
    "PLTR": "0001321655",
}

# 财年口径：报告和图表里必须标注，避免 FY 混用
FISCAL_YEAR = {
    "NVDA": "财年 1 月底结束（NVDA FY2026 ≈ 2025-01-27..2026-01-25）",
    "MSFT": "财年 6 月底结束（MSFT FY2026 = 2025-07-01..2026-06-30）",
    "PLTR": "财年 12 月底结束（= 自然年）",
}

SEC_MIN_INTERVAL = 0.15   # SEC 限速 10 req/s，留足余量
