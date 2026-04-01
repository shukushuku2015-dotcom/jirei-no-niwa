import feedparser

 

FEED_URL = "https://ideasforgood.jp/feed/"

 

def fetch_ideasforgood_articles():

    feed = feedparser.parse(

        FEED_URL,

        request_headers={

            "User-Agent": "Mozilla/5.0 (compatible; IdeasForGoodFetcher/1.0)"

        }

    )

 

    articles = []

 

    # パースエラーがあれば表示（デバッグ用）

    if feed.bozo:

        print("[IDEAS FOR GOOD] Feed parse error:", feed.bozo_exception)

 

    for entry in feed.entries:

        title = getattr(entry, "title", None)

        link = getattr(entry, "link", None)

        summary = getattr(entry, "summary", "") or ""

 

        if not title or not link:

            continue

 

        articles.append({

            "title": title.strip(),

            "lead": summary.strip(),

            "url": link.strip(),

            "published_at": None,

            "source": "ideasforgood"

        })

 

    print(f"[IDEAS FOR GOOD] fetched {len(articles)} items")

 

    return articles