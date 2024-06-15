import os
from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 설정
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST"),  # Docker 내부 네트워크에서 MySQL 컨테이너의 이름
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def get_database_connection():
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None
    
def fetch_data():
    connection = get_database_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    #######################################################
    #####################PHASE 2###########################
    #######################################################
    cursor.execute("SELECT title, date, writer, category, source, views, url FROM articles ORDER BY date DESC")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    formatted_data = []
    for row in rows:
        # date 객체를 'YYYY-MM-DD' 형식의 문자열로 변환
        formatted_date = row['date'].strftime('%Y-%m-%d') if isinstance(row['date'], date) else row['date']
        formatted_data.append({
            "title": row['title'],
            "date": formatted_date,
            "writer": row['writer'],
            "ctgry": row['category'],
            "source": row['source'],
            "views": row['views'],
            "url": row['url']
        })
    #######################################################
    #####################PHASE 2###########################
    #######################################################
    return formatted_data

@app.get("/data")
def read_data():
    data = fetch_data()
    return data


