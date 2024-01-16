import sqlite3
import pandas as pd

# CSVファイルのパス
file_path = '/Users/hayakawafutaba/Lecture/DSPR/DS_Pro/local.csv' 

# CSVファイルの読み込み
df = pd.read_csv('/Users/sakamotorio/dspro2/dspro2-1/local.csv')

# SQLiteデータベースの作成（または接続）
conn = sqlite3.connect('local.db')  # データベース名 local.db

# カーソルの作成
cursor = conn.cursor()

# テーブルの作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS walk_data (
        date TEXT,
        walk_hours INTEGER
    )
''')

# CSVからデータを読み込み、データベースに挿入
df.to_sql('walk_data', conn, if_exists='replace', index=False)

# 挿入されたデータの確認（オプション）
cursor.execute('SELECT * FROM walk_data')
inserted_data = cursor.fetchall()
for row in inserted_data:
    print(row)

# データベースとの接続を閉じる
conn.close()







