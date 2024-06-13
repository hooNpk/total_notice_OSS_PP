#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import traceback
import mysql.connector
from mysql.connector import Error

def get_skku_notices(base_url, start_date, end_date, type):
    notices = []
    page = 1
    date_text = start_date
    soup_paths = {
        "skku" : '#jwxe_main_content > div > div > div.container > div.board-name-list.board-wrap > ul',
        "sw_skku" : '#jwxe_main_content > div > div > div.board-name-list.board-wrap > ul'
    }

    while start_date <= date_text: # 날짜가 시작 날짜보다 이전이면 크롤링 종료
        try:
            #######################################################
            #####################PHASE 2###########################
            #######################################################
            headers = {
                "User-Agent": "curl/7.68.0"  # curl의 User-Agent 예시
            }
            response = requests.get(f"{base_url}{(page-1)*10}", headers=headers)
            #######################################################
            #####################PHASE 2###########################
            #######################################################
        except Exception as e:
            print(traceback.format_exc())
            print(e)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 공지사항 리스트 추출
        notice_elements = soup.select_one(
            soup_paths[type]
        ).children

        if not notice_elements:
            break

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
            full_link = base_url.split('?')[0] + link
            
            if start_date <= date_text <= end_date:
                article = {
                    "title": title_text,
                    "date": date_text,
                    "url": full_link,
                    "writer" : writer_text,
                    "category" : ctgry_text
                }
                if type=="skku":
                    article['source'] = "성균관대학교"
                elif type=="sw_skku":
                    article['source'] = "성균관대 소프트웨어융합대학"
                notices.append(article)
            else:
                continue  
        page += 1
    return notices

def insert_articles(df):
    try:
        # 데이터베이스 연결 설정
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),  # MySQL 컨테이너 이름
            database=os.getenv('DB_NAME'),  # 데이터베이스 이름
            user=os.getenv('DB_USER'),  # MySQL 사용자
            password=os.getenv('DB_PASSWORD'),  # MySQL 패스워드
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        # SQL 쿼리
        query = '''
        INSERT INTO articles (title, date, url, writer, category, source)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        
        # 데이터프레임의 행을 튜플로 변환하여 삽입
        for _, row in df.iterrows():
            cursor.execute(query, tuple(row))
        
        connection.commit()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # 연결 종료
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def main():
    # 크롤링할 URL 및 날짜 범위 설정
    # start_date = os.getenv('START_DATE')
    # end_date = os.getenv('END_DATE')
    start_date = "2024-05-30"
    end_date = "2024-06-13"
    skku_url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=list&&articleLimit=10&article.offset="
    sw_skku_url = "https://sw.skku.edu/sw/notice.do?mode=list&&articleLimit=10&article.offset="

    # 공지사항 크롤링
    notices = get_skku_notices(skku_url, start_date, end_date, "skku")
    sw_notices = get_skku_notices(sw_skku_url, start_date, end_date, "sw_skku")

    skku_df = pd.DataFrame(notices)
    skku_sw_df = pd.DataFrame(sw_notices)

    insert_articles(skku_df)
    insert_articles(skku_sw_df)

    #결과를 csv 파일로 저장. 이 CSV 파일을 읽어서 다른 container에 있는 mysql DB에 넣어줌.
    # skku_df.to_csv('/sharespace/skku_notices_240531-240531.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    main()