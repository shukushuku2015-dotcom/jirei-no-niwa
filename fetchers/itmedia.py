"""
itmedia.py

ITmedia の
- ビジネスオンライン RSS
- マーケティング RSS

から記事を取得し、
「企業・ブランドのマーケティング事例」と判断できるものだけを抽出する。

責務：
- 取得
- 判定
- 正規化（DB保存用フォーマット）

DB操作・UI操作は一切行わない
"""

import feedparser
import re
from datetime import datetime
from typing import List, Dict

# =========================
# RSS URL
# =========================

ITMEDIA_MARKETING_RSS = "https://rss.itmedia.co.jp/rss/2.0/marketing.xml"
ITMEDIA_BUSINESS_RSS  = "https://rss.itmedia.co.jp/rss/2.0/business.xml"

# =========================
# 正規表現（判定ルール）
# =========================

# 企業・ブランド名らしさ
BRAND_REGEX = re.compile(
    r"("
    r"[ァ-ヴー]{3,}"                 # カタカナ3文字以上
    r"|[A-Z]{2,}"                     # 英字略称（JCB, IBM 等）
    r"|ファミマ|セブン|ユニクロ|青山|マック|バーガーキング"
    r")"
)

# 事例・結果を示す語
CASE_PHRASE_REGEX = re.compile(
    r"(なぜ|理由|裏|勝ち筋|どう|突破|伸び|売れ|描く|成功)"
)

# 抽象論・ノウハウ除外
ABSTRACT_REGEX = re.compile(
    r"(とは何か|考え方|重要性|入門|基礎|必須|方法論|すべき)"
)

# 純ニュース・マクロ除外
NEWS_REGEX = re.compile(
    r"(決算|統計|指数|制度|法改正|市場全体)"
)

# =========================
# 判定関数
# =========================

def is_marketing_case(title: str) -> bool:
    """
    タイトルだけで
    「企業・ブランドのマーケティング事例か？」を判定する
    """

    if not title:
        return False

    # 除外（強）
    if ABSTRACT_REGEX.search(title):
        return False

    if NEWS_REGEX.search(title):
        return False

    # 必須条件
    has_brand = BRAND_REGEX.search(title)
    has_case_phrase = CASE_PHRASE_REGEX.search(title)

    return bool(has_brand and has_case_phrase)

# =========================
# RSS取得
# =========================

def fetch_rss(url: str, source: str) -> List[Dict]:
    feed = feedparser.parse(url)
    results = []

    now = datetime.now().isoformat(sep=" ", timespec="seconds")

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link")

        published = entry.get("published", "")
        if not published:
            published = ""

        results.append({
            "title": title,
            "lead": "",                  # RSSでは弱いため空
            "url": link,
            "published_at": published,
            "collected_at": now,
            "source": source,
        })

    return results

# =========================
# メイン取得関数
# =========================

def fetch_itmedia_cases() -> List[Dict]:
    """
    ITmedia Business + Marketing から
    事例判定に通ったものだけ返す
    """

    raw_articles: List[Dict] = []

    raw_articles.extend(
        fetch_rss(ITMEDIA_MARKETING_RSS, "itmedia")
    )
    raw_articles.extend(
        fetch_rss(ITMEDIA_BUSINESS_RSS, "itmedia")
    )

    cases: List[Dict] = []

    for article in raw_articles:
        if is_marketing_case(article["title"]):
            cases.append(article)

    return cases

# =========================
# 動作確認用
# =========================

if __name__ == "__main__":
    cases = fetch_itmedia_cases()

    print(f"ITmedia 抽出件数: {len(cases)}\n")

    for c in cases[:20]:
        print(f"- {c['title']}")
        print(f"  {c['url']}\n")