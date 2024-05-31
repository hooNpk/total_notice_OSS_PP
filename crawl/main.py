import requests
from bs4 import BeautifulSoup, NavigableString
#import pandas as pd
from datetime import datetime

def get_notices(base_url, start_date, end_date):
    notices = []
    page = 1
    while True:
        response = requests.get(f"{base_url}{(page-1)*10}")
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
                    "category" : ctgry_text
                })
            else:
                return notices  # 날짜가 시작 날짜보다 이전이면 크롤링 종료
        page += 1
    return notices

# 크롤링할 URL 및 날짜 범위 설정
url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=list&&articleLimit=10&article.offset="
start_date = "2024-05-30"  # 시작 날짜
end_date = "2024-05-31"  # 끝 날짜

# 공지사항 크롤링
notices = get_notices(url, start_date, end_date)
print(notices)

# # 데이터프레임으로 변환 후 출력
# df = pd.DataFrame(notices)
# print(df)

# # 결과를 csv 파일로 저장 (선택 사항)
# df.to_csv('skku_notices.csv', index=False)
