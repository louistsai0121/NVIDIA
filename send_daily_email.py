# -*- coding: utf-8 -*-
"""每日 NVIDIA 組織變化 + AI 商業影響新聞摘要信，供排程（本機或 GitHub Actions）每天呼叫。"""
import os
import smtplib
import sys
import urllib.request
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header

FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
SENDER = os.environ.get("GMAIL_ADDRESS", "")
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
RECIPIENT = os.environ.get("GMAIL_ADDRESS", "")

if not FIRECRAWL_API_KEY or not SENDER or not APP_PASSWORD:
    sys.exit("缺少環境變數：請設定 FIRECRAWL_API_KEY、GMAIL_ADDRESS、GMAIL_APP_PASSWORD")

SECTIONS = [
    ("內部組織變化", "NVIDIA organizational change leadership executive 黃仁勳 CEO 人事"),
    ("對 AI 商業的影響", "NVIDIA AI business impact stock market 輝達 AI 商業 影響"),
]


def firecrawl_search(query, limit=5):
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v2/search",
        data=json.dumps({"query": query, "limit": limit, "sources": ["news"]}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body.get("data", {}).get("news", []) or []


def format_section(title, results):
    lines = [f"【{title}】"]
    if not results:
        lines.append("今日無重大新消息。")
        return "\n".join(lines)
    seen_urls = set()
    for r in results:
        url = r.get("url", "")
        if url in seen_urls:
            continue
        seen_urls.add(url)
        headline = r.get("title", "(無標題)")
        snippet = r.get("description") or r.get("snippet") or ""
        lines.append(f"- {headline}")
        if snippet:
            lines.append(f"  {snippet}")
        if url:
            lines.append(f"  {url}")
    return "\n".join(lines)


def build_body():
    parts = []
    for title, query in SECTIONS:
        try:
            results = firecrawl_search(query)
        except Exception as exc:
            results = []
            parts.append(f"【{title}】\n（本區塊搜尋失敗：{exc}）")
            continue
        parts.append(format_section(title, results))
    parts.append(
        "\n---\n此信由本機排程腳本自動產生，內容為 Firecrawl 新聞搜尋原始結果整理，未經 AI 重新摘要。"
    )
    return "\n\n".join(parts)


def send_email(body, today):
    subject = f"NVIDIA 動態摘要 {today}"
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, APP_PASSWORD)
        server.sendmail(SENDER, [RECIPIENT], msg.as_string())


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    body = build_body()
    send_email(body, today)
    print("SENT_OK")


if __name__ == "__main__":
    main()
