from fetchers.rss_base import fetch_from_rss

RSS_URL = "https://predge.jp/feed/"

def fetch_predge_articles():
    """
    PR EDGE を RSS で取得し、
    共通フォーマットの記事リストを返す
    """
    return fetch_from_rss(
        source_id="predge",
        rss_url=RSS_URL,
        max_items=30
    )