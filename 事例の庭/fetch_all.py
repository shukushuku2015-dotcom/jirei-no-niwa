from fetch_xtrend_article import fetch_xtrend_articles
from fetchers.advertimes import fetch_advertimes_articles
from fetchers.predge import fetch_predge_articles
from fetchers.ideasforgood import fetch_ideasforgood_articles
from fetchers.itmedia import fetch_itmedia_cases   # ★追加
from common_db import save_article, url_exists


def log_and_extend(all_articles, source_name, articles):
    print(f"<< {source_name}: 取得 {len(articles)} 件")
    all_articles.extend(articles)


def main():
    print("=== 全ソース取得開始 ===")
    all_articles = []

    # =========================
    # AdverTimes（RSS）
    # =========================
    print(">> AdverTimes start")
    advertimes_articles = fetch_advertimes_articles()
    log_and_extend(all_articles, "AdverTimes", advertimes_articles)

    # =========================
    # PR EDGE（RSS）
    # =========================
    print(">> PR EDGE start")
    predge_articles = fetch_predge_articles()
    log_and_extend(all_articles, "PR EDGE", predge_articles)

    # =========================
    # IDEAS FOR GOOD（RSS）
    # =========================
    print(">> IDEAS FOR GOOD start")
    ideas_articles = fetch_ideasforgood_articles()
    log_and_extend(all_articles, "IDEAS FOR GOOD", ideas_articles)

    # =========================
    # ITmedia（Business / Marketing RSS）
    # =========================
    print(">> ITmedia start")
    itmedia_articles = fetch_itmedia_cases()
    log_and_extend(all_articles, "ITmedia", itmedia_articles) 

    # =========================
    # 日経クロストレンド（HTML）
    # =========================
    print(">> XTrend start")
    xtrend_articles = fetch_xtrend_articles()
    log_and_extend(all_articles, "XTrend", xtrend_articles)



    # =========================
    # DB保存
    # =========================
    saved = 0
    skipped = 0

    for article in all_articles:
        if url_exists(article["url"]):
            skipped += 1
            continue
        save_article(article)
        saved += 1

    print("=== 保存結果 ===")
    print(f"保存: {saved}")
    print(f"スキップ: {skipped}")
    print("=== 完了 ===")


if __name__ == "__main__":
    main()