import json
from datetime import timedelta

import pandas as pd
import requests
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook

# Константы
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL_TEMPLATE = "https://hacker-news.firebaseio.com/v0/item/{}.json"
LOCAL_FILE_PATH = "/opt/airflow/data/hn_top_stories.json"
PROCESSED_CSV_PATH = "/opt/airflow/data/processed_hn_stories.csv"
PARQUET_FILE_PATH = "/opt/airflow/data/hn_stories.parquet"


def download_data():
    """
    Функция получения данных с Hacker News API
    (топ-20 историй с полной информацией)
    """

    response = requests.get(TOP_STORIES_URL)
    if response.status_code == 200:
        story_ids = response.json()[:20]

        stories = []
        for sid in story_ids:
            item_resp = requests.get(ITEM_URL_TEMPLATE.format(sid))
            if item_resp.status_code == 200:
                story = item_resp.json()
                if story and story.get("type") == "story":
                    stories.append(story)

        with open(LOCAL_FILE_PATH, "w") as file:
            json.dump(stories, file, ensure_ascii=False)
    else:
        raise Exception(
            f"Error fetching top stories from Hacker News API: {response.status_code}"
        )


def process_data():
    """
    Функция очистки и преобразования загруженных данных
    """
    with open(LOCAL_FILE_PATH, "r") as file:
        stories = json.load(file)

    df = pd.json_normalize(stories)

    df["url"] = df["url"].fillna("")
    df["title"] = df["title"].fillna("No title")
    df["by"] = df["by"].fillna("anonymous")
    df["score"] = df["score"].fillna(0).astype(int)
    df["descendants"] = df["descendants"].fillna(0).astype(int)
    df["time"] = df["time"].fillna(0).astype(int)
    df["type"] = df["type"].fillna("story")

    # Оставляем только нужные колонки
    df = df[["id", "title", "url", "score", "by", "time", "descendants", "type"]]

    df.to_csv(PROCESSED_CSV_PATH, index=False)


def save_data():
    """
    Функция сохранения данных в parquet-файл
    """
    processed_df = pd.read_csv(PROCESSED_CSV_PATH)
    processed_df.to_parquet(PARQUET_FILE_PATH)


def export_to_postgres():
    """
    Функция сохранения данных в Postgres БД
    """
    df = pd.read_csv(PROCESSED_CSV_PATH)

    hook = PostgresHook(postgres_conn_id="postgres_hn")
    conn = hook.get_conn()
    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO hn_stories
            (id, title, url, score, by, time, descendants, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["id"],
                row["title"],
                row["url"],
                row["score"],
                row["by"],
                row["time"],
                row["descendants"],
                row["type"],
            ),
        )

    # Commit транзакций к БД
    conn.commit()
    cursor.close()
    conn.close()


default_args = {
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
    "start_date": days_ago(1),
}


with DAG(
    "hack_news_pipeline_dag",
    default_args=default_args,
    description="Пайплайн получения топ-сторис из Hacker News API",
    schedule_interval="0 21 * * *",
    catchup=False,
    tags=["hackernews"],
) as dag:

    download_data_task = PythonOperator(
        task_id="download_data",
        python_callable=download_data,
    )

    process_data_task = PythonOperator(
        task_id="process_data",
        python_callable=process_data,
    )

    save_data_task = PythonOperator(
        task_id="save_data",
        python_callable=save_data,
    )

    create_hn_table = PostgresOperator(
        task_id="create_hn_table",
        postgres_conn_id="postgres_hn",
        sql="""
        CREATE TABLE IF NOT EXISTS hn_stories (
            id BIGINT,
            title TEXT,
            url TEXT,
            score INTEGER,
            by VARCHAR(100),
            time BIGINT,
            descendants INTEGER,
            type VARCHAR(20)
        );
        """,
    )

    export_to_db = PythonOperator(
        task_id="export_to_db",
        python_callable=export_to_postgres,
    )

    [download_data_task, create_hn_table] >> process_data_task >> save_data_task >> export_to_db