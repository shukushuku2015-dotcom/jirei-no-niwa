from fetchers.rss_base import fetch_from_rss

RSS_URL = "https://www.advertimes.com/feed/"

def fetch_advertimes_articles():
    """
    AdverTimes（アドタイ）をRSSで取得し、
    共通フォーマットの記事リストを返す。
    """
    return fetch_from_rss(
        source_id="advertimes",
        rss_url=RSS_URL,
        max_items=30
    )