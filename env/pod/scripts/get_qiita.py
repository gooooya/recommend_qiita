#!/usr/bin/env python
# coding: utf-8

# ドキュメント
# https://qiita.com/api/v2/docs
# 
# ページング(page)の最大数は100,1ページ当たりの件数(per_page)最大数も100

import os
import requests
import psycopg2
import psycopg2.extras
from dateutil import parser
from datetime import timezone
from datetime import timezone, timedelta

DATABASE_URL = "postgresql://{}:{}@postgres-service:{}/{}".format(
    os.environ['POSTGRES_USER'], 
    os.environ['POSTGRES_PASSWORD'], 
    os.environ['POSTGRES_SERVICE_SERVICE_PORT'], 
    os.environ['POSTGRES_DB'])

JST = timezone(timedelta(hours=9))

def fetch_qiita_articles(page=1, per_page=100):
    """Qiitaの記事を取得する"""
    url = f'https://qiita.com/api/v2/items?page={page}&per_page={per_page}'
    qiita_token = os.environ['QIITA_TOKEN']
    headers = {'Authorization': f'Bearer {qiita_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def insert_articles(articles):
    """記事のリストをデータベースに挿入する"""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, 
                "INSERT INTO learning_resources (title, url, created_date) VALUES (%s, %s, %s)  ON CONFLICT (url) DO NOTHING",
                [(article['title'], article['url'], parser.parse(article['created_at']).replace(tzinfo=None)) for article in articles])

def get_article_time_bounds_from_db():
    """DBに格納されている最新記事と最古記事の作成日時(日本時間)を取得"""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(created_date), MIN(created_date) FROM learning_resources")
            max_created_date, min_created_date = cur.fetchone()
            max_created_date = max_created_date.astimezone(JST) if max_created_date else None
            min_created_date = min_created_date.astimezone(JST) if min_created_date else None
            return max_created_date, min_created_date

def main():
    """取得上限まで記事を取得し、DBにインサート"""
    for i in range(1, 101):
        last_fetch_time_jst, first_fetch_time_jst = get_article_time_bounds_from_db()
        articles = fetch_qiita_articles(page=i)
        if articles:
            filtered_articles = []
            for article in articles:
                article_time_jst = parser.parse(article['created_at']).astimezone(JST)
                if last_fetch_time_jst is None or article_time_jst > last_fetch_time_jst:
                    filtered_articles.append(article)
                elif first_fetch_time_jst or article_time_jst < first_fetch_time_jst:
                    filtered_articles.append(article)
            if filtered_articles:
                insert_articles(filtered_articles)
            else:
                # 範囲外の記事がない場合、処理を終了する
                break

if __name__ == "__main__":
    main()