import feedparser
from bs4 import BeautifulSoup

def fetch_from_rss(source_id, rss_url, max_items=30):
    """
    RSSフィードを取得し、共通フォーマットで記事候補を返す。
    媒体差を吸収するため、取り方は最大限ロバストにしている。
    """
    feed = feedparser.parse(rss_url)
    articles = []

    if not feed.entries:
        print(f"[{source_id}] RSS entries が空です")
        return articles

    for entry in feed.entries[:max_items]:
        title = entry.get("title", "").strip()
        url = entry.get("link", "").strip()

        # 日付（無い場合もある）
        published = (
            entry.get("published")
            or entry.get("pubDate")
            or ""
        )

        # 概要（description / summary の揺れ吸収）
        summary_html = (
            entry.get("description")
            or entry.get("summary")
            or ""
        )

        soup = BeautifulSoup(summary_html, "html.parser")
        lead = soup.get_text(strip=True)

        if not title or not url:
            continue

        articles.append({
            "source": source_id,
            "url": url,
            "title": title,
            "published_at": published,
            "lead": lead,
        })

    return articles
