import streamlit as st
import sqlite3
import math
import time
import html  # ★追加
from datetime import datetime, date

# ★追加：favorites 用
from common_db import add_favorite, remove_favorite, load_favorite_urls

# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="事例収集の庭",
    layout="wide"
)

# =========================
# DB 接続（★変更：mode 対応）
# =========================
def load_cases(mode="all"):
    conn = sqlite3.connect("cases.db")
    conn.row_factory = sqlite3.Row

    if mode == "favorites":
        rows = conn.execute("""
            SELECT
                title,
                lead,
                url,
                published_at,
                collected_at,
                source
            FROM cases
            WHERE url IN (SELECT url FROM favorites)
            AND source IS NOT NULL
            ORDER BY collected_at DESC
        """).fetchall()
    else:
        rows = conn.execute("""
            SELECT
                title,
                lead,
                url,
                published_at,
                collected_at,
                source
            FROM cases
            WHERE source IS NOT NULL
            ORDER BY collected_at DESC
        """).fetchall()

    conn.close()
    return rows

# =========================
# ★追加：保存記事トグルの初期化
# =========================
if "show_favorites" not in st.session_state:
    st.session_state["show_favorites"] = False

# =========================
# ★追加：保存記事トグルボタン
# =========================
toggle_label = "⭐ 保存記事のみ表示" if not st.session_state["show_favorites"] else "📄 全件表示に戻す"

if st.button(toggle_label):
    st.session_state["show_favorites"] = not st.session_state["show_favorites"]
    st.rerun()

# =========================
# ヘッダー（タイトル＋更新＋検索）
# =========================
title_col, refresh_col, search_col = st.columns([3, 1, 2])

with title_col:
    st.title("🌱 事例収集の庭")

with refresh_col:
    if st.button("🔄 最新に更新"):
        st.toast("最新データを読み込みました")
        time.sleep(0.3)
        st.rerun()

with search_col:
    search_query = st.text_input(
        "",
        placeholder="タイトル・キャプションで検索"
    )

# ★変更：モードをトグル状態から決定
mode_key = "favorites" if st.session_state["show_favorites"] else "all"

cases = load_cases(mode_key)

# =========================
# 検索
# =========================
def match(case):
    if not search_query:
        return True
    q = search_query.lower()
    return (
        q in (case["title"] or "").lower()
        or q in (case["lead"] or "").lower()
    )

filtered = [c for c in cases if match(c)]

# =========================
# ページネーション
# =========================
PER_PAGE = 50
total_pages = max(1, math.ceil(len(filtered) / PER_PAGE))

page = st.number_input(
    "ページ",
    min_value=1,
    max_value=total_pages,
    step=1
)

start = (page - 1) * PER_PAGE
end = start + PER_PAGE
page_cases = filtered[start:end]

# =========================
# source 別カラー
# =========================
SOURCE_COLORS = {
    "xtrend": "#E8F2FF",
    "advertimes": "#FFF3E0",
    "predge": "#F2F2F2",
    "ideasforgood": "#E8F5E9",
    "itmedia": "#F3F6FA",      # ★追加
}

SOURCE_LABELS = {
    "xtrend": "日経クロストレンド",
    "advertimes": "AdverTimes",
    "predge": "PR EDGE",
    "ideasforgood": "IDEAS FOR GOOD",
    "itmedia": "ITmedia",     # ★追加
}

today = date.today()

# =========================
# カード表示（Phase A：左色付けのみ）
# =========================
cols = st.columns(3)

# ★追加：保存済み URL 一括取得
favorite_urls = set(load_favorite_urls())

for i, case in enumerate(page_cases):
    col = cols[i % 3]

    bg = SOURCE_COLORS.get(case["source"], "#FFFFFF")
    label = SOURCE_LABELS.get(case["source"], "")

    collected_date = datetime.fromisoformat(case["collected_at"]).date()
    is_today = collected_date == today

    border_color = "#4CAF50" if is_today else "transparent"

    safe_title = html.escape(case["title"] or "")
    safe_lead = html.escape(case["lead"] or "").replace("\n", "<br>")

    url = case["url"]
    is_fav = url in favorite_urls

    with col:
        # ★追加：保存ボタン
        if is_fav:
            if st.button("★ 保存済み（解除）", key=f"unfav_{url}"):
                remove_favorite(url)
                st.rerun()
        else:
            if st.button("☆ 保存する", key=f"fav_{url}"):
                add_favorite(url)
                st.rerun()

        st.markdown(
            f"""
            <div style="
                background:{bg};
                padding:18px;
                border-radius:12px;
                margin-bottom:20px;
                box-shadow:0 2px 6px rgba(0,0,0,0.1);
                border-left:6px solid {border_color};
            ">
                <div style="font-size:11px;color:#666;">
                    {label}
                </div>
                <h3 style="margin:8px 0; font-size:20px;">
                    <a href="{case['url']}" target="_blank"
                       style="color:inherit;text-decoration:none;">
                        {safe_title}
                    </a>
                </h3>
                <p style="color:#444; line-height:1.6;">
                    {safe_lead}
                </p>
                <div style="font-size:10px;color:#888;">
                    公開日: {case['published_at']
                          if case['published_at']
                          else case['collected_at'].split(" ")[0]
                    } /
                    収集日: {case['collected_at']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.caption(f"全 {len(filtered)} 件 / {page} ページ目")