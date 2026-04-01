"""
RSSソース定義ファイル

ここにRSS情報収集ソースをすべて集約する。
fetcher側は、この定義を読むだけでよい。
"""

RSS_SOURCES = {
    # =========================
    # 国内（最優先）
    # =========================

    "markezine": {
        "name": "MarkeZine",
        "rss_url": "https://markezine.jp/rss/new/20/index.xml",
        "priority": "A",
        "note": "MVPの主食。安定・高品質・ログイン不要。",
    },

    "webtan": {
        "name": "Web担当者Forum",
        "rss_url": "https://webtan.impress.co.jp/rss.xml",
        "priority": "A",
        "note": "デジタル施策事例の安定供給源。",
    },

    "advertimes": {
        "name": "AdverTimes（アドタイ）",
        "rss_url": "https://www.advertimes.com/feed/",
        "priority": "B",
        "note": "広告・キャンペーン速報枠。",
    },

    "predge": {
        "name": "PR EDGE",
        "rss_url": "https://predge.jp/feed/",
        "priority": "B",
        "note": "国内外の事例を日本語で整理。MVPで映える。",
    },

    "ideasforgood": {
        "name": "IDEAS FOR GOOD",
        "rss_url": "https://ideasforgood.jp/feed/",
        "priority": "C",
        "note": "サステナブル・社会文脈補完。",
    },

    # =========================
    # 海外（MVPは少数精鋭）
    # =========================

    "adage": {
        "name": "Ad Age",
        "rss_url": "https://adage.com/rss.xml",
        "priority": "A",
        "note": "海外広告・ブランド文脈のアンカー。",
    },

    "thedrum": {
        "name": "The Drum",
        "rss_url": "https://www.thedrum.com/rss.xml",
        "priority": "A",
        "note": "事例粒度が高く、企画視点で使いやすい。",
    },

    "fastcompany_brand": {
        "name": "Fast Company（Brand）",
        "rss_url": "https://www.fastcompany.com/rss",
        "priority": "B",
        "note": "テック×ブランド補完枠。",
    },
}
