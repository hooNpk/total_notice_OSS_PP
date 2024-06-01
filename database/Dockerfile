# mysql database 띄우기

# 베이스 이미지로 MySQL 사용
FROM mysql:latest

# 환경 변수 설정
ENV MYSQL_ROOT_PASSWORD=best-oss-class
ENV MYSQL_DATABASE=tndb
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=best-student

# 초기 데이터베이스 설정을 위한 스크립트 복사
COPY ./init.sql /docker-entrypoint-initdb.d/

# MySQL 서버 시작
CMD ["mysqld"]