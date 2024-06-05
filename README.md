## Total Notice Page OSS PP
- 이 프로젝트는 2024년 1학기 성균관대학교 오픈소스소프트웨어실습 개인 프로젝트로 시작하였습니다.
- 성균관대학교 웹사이트에 흩어져 있는 공지를 모아 하나의 페이지에서 볼 수 있습니다.
- shell을 사용하여 컨테이너 기반의 서버와 데이터베이스를 쉽게 띄울 수 있습니다.

### 프로젝트 데모
![프로젝트 데모](https://github.com/hooNpk/total_notice_OSS_PP/blob/main/assets/Total-Notice.gif)
  
---
  
### 요약
- 소프트웨어학과인 저는 세 개의 공지 페이지를 봐야합니다. 소프트웨어학과 공지 페이지, 소프트웨어융합대학 공지 페이지, 성균관대학 공지페이지입니다.
- 공지 페이지에는 유용한 정보가 올라오기 때문에 챙겨봐야 하지만 세 개 페이지를 다 들어가는 건 **귀찮습니다**. 그래서 여러 곳의 공지를 한꺼번에 볼 수 있는 페이지를 만들었습니다.
- 이 프로젝트는 네 개의 컨테이너로 구성되어 있습니다.
    - **tn-crawl** : 공지를 크롤링해와 tn-sql 컨테이너에 있는 데이터베이스에 저장. crawl 폴더.
    - **tn-sql** : mysql 데이터베이스가 들어있는 컨테이너. database 폴더.
    - **tn-back** : tn-sql 데이터베이스를 참조하여 뿌려주는 fastapi 서버 컨테이너. webpage/backend 폴더
    - **tn-front** : React 기반의 웹페이지를 제공하는 컨테이너. webpage/frontend 폴더
    - **tn은 Total Notice**의 줄인말입니다.
---

### 코드 설명
- 

---

### 사용방법
1. 각 컨테이너 관련 리소스의 위치
    1. crawl, database, webpage 디렉토리가 있습니다.
    1. tn-crawl과 관련된 모든 리소스는 crawl 디렉토리에 있습니다.
    1. tn-sql과 관련된 리소스는 database 디렉토리에 있습니다.
    1. 웹페이지 관련된 리소스는 webpage 디렉토리에 있습니다.
1. 레포지토리를 clone 합니다
    ```bash
    $ git clone https://github.com/hooNpk/total_notice_OSS_PP
    cd total_notice_OSS_PP
    ```
1. tn-sql 컨테이너를 띄웁니다. 설정은 `database/Dockerfile`, `database/init.sql`에 있습니다.
    ```bash
    $ bash databse/db.sh
    ```
1. tn-crawl 컨테이너를 띄운 뒤 크롤링할 날짜를 입력하세요. `crawl/Dockerfile`을 참고하세요. 
    ```bash
    $ bash crawl/crawl.sh
    $ 2024-05-30
    $ 2024-06-03
    ```
1. tn-back 컨테이너와 tn-front 컨테이너를 띄웁니다. `webpage/backend/Dockerfile`, `webpage/frontend/Dockerfile`을 참고하세요.
    ```bash
    $ bash webpage/webpage.sh
    ```
1. 웹 브라우저에서 `127.0.0.1`에 접속합니다.
![사용방법]()

---

### 이 프로젝트 기여하는 방법
- 커밋은 commitizen 라이브러리를 사용해서 규격화하여 남겨주세요. [링크](https://pypi.org/project/commitizen/)
- dev 브랜치에서 분기하여 새로운 branch를 만들어 개발하고 기능이 완성되면 PR을 남겨주세요.
- 새로운 branch를 만들 때는 만든 기능이 명확하게 드러날 수 있도록 이름을 지어주세요. 예로 들어 다른 학과나 대학의 공지를 크롤링 할 수 있도록 추가하였다면 add-crawl로 브랜치 이름을 지어주세요.
- 버그가 있다면 Issues에 남겨주세요. 빠르게 대응하겠습니다.

---

### 개선하거나 추가할 수 있는 기능
- 웹페이지를 보여주는 부분에 좀 더 기능을 넣을 수 있습니다. 검색 기능을 넣거나 웹 페이지를 예쁘게 만들 수 있습니다.
- 원하는 공지가 올라왔을 때 알림을 줄 수도 있습니다. 메일을 보내거나, 카카오톡 메시지를 보낼 수 있습니다.
- 공지를 크롤링할 때 gpt api를 사용하여 데이터 레이블링을 한 뒤 추가적인 분류를 하여 웹 페이지에서 보여줄 수 있습니다.
- 다른 학과나 단과 대학의 공지를 크롤링 할 수 있습니다. 지금은 성균관대학교, 성균관대 소프트웨어융합대학의 공지만을 크롤링해옵니다.

---

### 참고
- 데이터베이스에 접근하는 방법
- tn-sql 컨테이너를 띄운 뒤 다음 코드 실행
    ```bash
    docker exec -it tn-sql mysql -u admin -p
    ```
    ```sql
    USE tndb;
    SELECT * FROM articles;
    ```