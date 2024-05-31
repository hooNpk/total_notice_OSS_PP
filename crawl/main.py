#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import traceback

def get_skku_notices(base_url, start_date, end_date):
    notices = []
    page = 1
    date_text = start_date
    while start_date <= date_text: # 날짜가 시작 날짜보다 이전이면 크롤링 종료
        try:
            response = requests.get(f"{base_url}{(page-1)*10}")
        except Exception as e:
            print(traceback.format_exc())
            print(e)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 공지사항 리스트 추출
        notice_elements = soup.select_one(
            '#jwxe_main_content > div > div > div.container > div.board-name-list.board-wrap > ul'
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
                notices.append({
                    "title": title_text,
                    "date": date_text,
                    "url": full_link,
                    "writer" : writer_text,
                    "category" : ctgry_text,
                    "source" : "skku"
                })
            else:
                continue  
        page += 1
    return notices

# 크롤링할 URL 및 날짜 범위 설정
skku_url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=list&&articleLimit=10&article.offset="
start_date = "2024-05-30"  # 시작 날짜
end_date = "2024-05-31"  # 끝 날짜

# 공지사항 크롤링
notices = get_skku_notices(skku_url, start_date, end_date)

# TODO 소프트웨어대학, 소프트웨어학과 공지사항 크롤링
# 소프트웨어대학 공지사항 : https://sw.skku.edu/sw/notice.do?mode=list&&articleLimit=10&article.offset=20
# 소프트웨어학과 공지사항 : https://cse.skku.edu/cse/notice.do

# 이걸 데이터프레임 형태로 만들어서 csv 저장. 
# 현재 디렉토리 기준으로 해서 volume을 설정해야 할 듯
# mysql 관련 컨테이너에서 집어넣자
# # 데이터프레임으로 변환 후 출력
df = pd.DataFrame(notices)

#결과를 csv 파일로 저장
#csv를 읽어와서 mysql database에 넣어주는 건 다른 container에서 실행
df.to_csv('/sharespace/skku_notices_240531-240531.csv', index=False, encoding='utf-8')
