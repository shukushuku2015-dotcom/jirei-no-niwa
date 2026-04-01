import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://markezine.jp"
LIST_URL = "https://markezine.jp/list"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_article_urls(max_pages=3):
    """
    記事一覧ページから記事URLを取得
    """
    urls = []

    for page in range(1, max_pages + 1):
        url = f"{LIST_URL}/search?page={page}"

        try:
            res = requests.get(url, headers=HEADERS, timeout=(5, 15))
        except Exception:
            continue

        if res.status_code != 200:
            continue

        soup = BeautifulSoup(res.text, "html.parser")

        for a in soup.select("a[href^='/article/detail/']"):
            href = a.get("href")
            full_url = urljoin(BASE_URL, href)
            if full_url not in urls:
                urls.append(full_url)

        time.sleep(1)

    return urls


def fetch_article(url):
    """
    記事ページから title / lead / published_at を取得
    """
    try:
        res = requests.get(url, headers=HEADERS, timeout=(5, 15))
    except Exception:
        return None

    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    # タイトル
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # 日付
    date_tag = soup.select_one("time")
    published_at = date_tag.get_text(strip=True) if date_tag else ""

    # リード文（最初の p を使用）
    lead = ""
    for p in soup.select("div.article-body p"):
        text = p.get_text(strip=True)
        if len(text) >= 50:
            lead = text
            break

    if not title or not lead:
        return None

    return {
        "source": "markezine",
        "url": url,
        "title": title,
        "published_at": published_at,
        "lead": lead,
    }


def fetch_markezine_articles():
    """
    fetch_all.py から呼ばれるエントリポイント
    """
    urls = fetch_article_urls()
    articles = []

    for i, url in enumerate(urls, start=1):
        print(f"[MarkeZine] 処理中 {i}/{len(urls)}")

        article = fetch_article(url)
        if article:
            articles.append(article)

    print(f"[MarkeZine] 取得候補数: {len(articles)}")
    return articles
