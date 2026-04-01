import sqlite3

import os

from openai import OpenAI

 

# ===== 設定 =====

DB_NAME = "cases.db"

 

# 環境変数から APIキーを読む

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

 

def get_one_case():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

 

    row = cur.execute(

        "SELECT id, title, lead FROM cases ORDER BY id LIMIT 1"

    ).fetchone()

 

    conn.close()

    return row

 

def summarize(title, lead):

    prompt = f"""

以下の記事を日本語で要約してください。

 

条件：

- 150〜200文字

- 宣伝文句にしない

- 事実ベース

- 第三者視点

 

【タイトル】

{title}

 

【本文】

{lead}

"""

 

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {"role": "user", "content": prompt}

        ]

    )

 

    return response.choices[0].message.content.strip()

 

if __name__ == "__main__":

    case = get_one_case()

 

    if not case:

        print("DBに事例がありません")

        exit()

 

    case_id, title, lead = case

 

    print("対象記事")

    print("--------")

    print(title)

    print("")

 

    summary = summarize(title, lead)

 

    print("要約結果")

    print("--------")

    print(summary)