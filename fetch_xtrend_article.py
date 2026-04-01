import requests

import time

from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse, urlunparse

# ★追加：タイトル重複チェック
from common_db import title_exists


# ====================
# 設定
# ====================

TOP_URL = "https://xtrend.nikkei.com/"

HEADERS = {

    "User-Agent": "Mozilla/5.0"

}

NG_KEYWORDS = ["一覧", "特集", "動画", "セミナー", "講座", "デザイン"]


# ====================
# トップページから記事URL取得
# ====================

def fetch_article_urls():

    res = requests.get(

        TOP_URL,

        headers=HEADERS,

        timeout=(5, 15)

    )

    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    urls = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/atcl/" in href:
            full_url = urljoin(TOP_URL, href)

            parsed = urlparse(full_url)
            normalised_url = urlunparse(
                (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
            )

            urls.add(normalised_url)

    return list(urls)


# ====================
# 個別記事取得
# ====================

def fetch_article(url):

    try:

        res = requests.get(

            url,

            headers=HEADERS,

            timeout=(5, 15)

        )

    except Exception as e:

        print("  →通信失敗スキップ:", e)

        return None

    if res.status_code != 200:

        return None

    soup = BeautifulSoup(res.text, "html.parser")

    title_tag = soup.find("h1")

    title = title_tag.get_text(strip=True) if title_tag else ""

    time_tag = soup.find("time")

    published_at = (

        time_tag["datetime"]

        if time_tag and time_tag.has_attr("datetime")

        else ""

    )

    lead = ""

    for p in soup.find_all("p"):

        text = p.get_text(strip=True)

        if len(text) >= 50:

            lead = text

            break

    return {

        "url": url,

        "title": title,

        "published_at": published_at,

        "lead": lead

    }


# ====================
# 記事フィルタ
# ====================

def is_valid_article(article):

    if len(article["title"]) < 6:

        return False

    if len(article["lead"]) < 50:

        return False

    for ng in NG_KEYWORDS:

        if ng in article["title"]:

            return False

    return True


# ====================
# fetch_all.py から呼ばれる関数（★重要）
# ====================

def fetch_xtrend_articles():

    """
    DBを見ずに、日経クロストレンドの記事候補を
    すべて取得してリストで返す
    """

    urls = fetch_article_urls()

    articles = []

    for i, url in enumerate(urls, start=1):

        print(f"[XTrend]処理中 {i}/{len(urls)}")

        article = fetch_article(url)

        if article and is_valid_article(article):

            # ★追加：タイトル重複ならスキップ
            if title_exists(article["title"]):
                continue

            article["source"] = "xtrend"

            articles.append(article)

        time.sleep(1)

    print(f"[XTrend]取得候補数: {len(articles)}")

    return articles