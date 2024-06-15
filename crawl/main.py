#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import traceback
import mysql.connector
from mysql.connector import Error

#######################################################
#####################PHASE 2###########################
#######################################################

types = {
    "skku" : "성균관대학교",
    "sw_skku" : "성균관대 소프트웨어융합대학"
}

def crawl_by_pages(start_date, end_date, type):
    """
    page 별로 공지사항을 크롤링할 수 있도록 분기해주는 함수
    모든 공지사항을 다 받아온 뒤 데이터베이스에 넣지 않고 page 별로 넣어서
    중간에 에러가 발생해도 그 전까지의 데이터는 저장할 수 있도록 함
    """
    did_insert = False
    page = 1
    soup_paths = {
        "skku" : '#jwxe_main_content > div > div > div.container > div.board-name-list.board-wrap > ul',
        "sw_skku" : '#jwxe_main_content > div > div > div.board-name-list.board-wrap > ul'
    }
    base_urls = {
        "skku" : "https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=list&&articleLimit=10&article.offset=",
        "sw_skku" : "https://sw.skku.edu/sw/notice.do?mode=list&&articleLimit=10&article.offset="
    }

    date_text = start_date
    while start_date <= date_text:
        target_url = f"{base_urls[type]}{(page-1)*10}"
        notices = crawl_notices(target_url, soup_paths[type], start_date, end_date)
        if did_insert and not notices:
            break
        if notices:
            date_text = notices[-1]['date']
            df_notices = pd.DataFrame(notices)
            insert_articles(df_notices, type)
            did_insert = True
        page += 1
        
#######################################################
#####################PHASE 2###########################
#######################################################



def crawl_notices(target_url, soup_path, start_date, end_date):
    """
        주어진 URL에 대해서만 공지사항을 크롤링하도록 변경
    """
    notices = []
    
    try:
        #######################################################
        #####################PHASE 2###########################
        #######################################################
        headers = {
            "User-Agent": "curl/7.68.0"  # curl의 User-Agent 예시
        }
        response = requests.get(target_url, headers=headers)
        #######################################################
        #####################PHASE 2###########################
        #######################################################
    except Exception as e:
        print(traceback.format_exc())
        print(e)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 공지사항 리스트 추출
    notice_elements = soup.select_one(
        soup_path
    ).children

    if not notice_elements:
        return []

    for notice in notice_elements:
        if isinstance(notice, NavigableString):
            continue
        ctgry = notice.select_one('dl > dt > span.c-board-list-category')
        ctgry_text = ctgry.text.strip() if ctgry else None
        title = notice.select_one('dl > dt > a')
        title_text = title.text.strip()
        link = title['href']
        writer = notice.select_one('dl > dd > ul > li:nth-child(2)')
        writer_text = writer.text.strip()
        date = notice.select_one('dl > dd > ul > li:nth-child(3)')
        date_text = date.text.strip()
        full_link = target_url.split('?')[0] + link
        
        if start_date <= date_text and date_text <= end_date:
            article = {
                "title": title_text,
                "date": date_text,
                "url": full_link,
                "writer" : writer_text,
                "category" : ctgry_text
            }
            notices.append(article)
        else:
            continue  
    return notices

def insert_articles(df, type):
    try:
        # 데이터베이스 연결 설정
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),  # MySQL 컨테이너 이름
            database=os.getenv('DB_NAME'),  # 데이터베이스 이름
            user=os.getenv('DB_USER'),  # MySQL 사용자
            password=os.getenv('DB_PASSWORD'),  # MySQL 패스워드
            charset='utf8mb4'
        )
        # 로컬 개발용 데이터베이스 연결 설정
        # connection = mysql.connector.connect(
        #     host='127.0.0.1',  # MySQL 컨테이너 이름
        #     database='tndb',  # 데이터베이스 이름
        #     user='admin',  # MySQL 사용자
        #     password='best-student',  # MySQL 패스워드
        #     charset='utf8mb4'
        # )
        cursor = connection.cursor()
        
        # SQL 쿼리
        query = '''
        INSERT INTO articles
        (title, date, url, writer, category, source)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''

        # 데이터프레임의 행을 튜플로 변환하여 삽입
        for _, row in df.iterrows():
            row['source'] = types[type]
            cursor.execute(query, tuple(row))
        
        connection.commit()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # 연결 종료
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def main():
    # 크롤링할 URL 및 날짜 범위 설정
    start_date = os.getenv('START_DATE')
    end_date = os.getenv('END_DATE')
    # start_date = "2024-06-12"
    # end_date = "2024-06-13"
    

    # 공지사항 크롤링
    crawl_by_pages(start_date, end_date, "skku")
    crawl_by_pages(start_date, end_date, "sw_skku")
    return

if __name__ == "__main__":
    main()