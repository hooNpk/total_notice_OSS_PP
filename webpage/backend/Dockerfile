
FROM python:3.10-slim
WORKDIR /app

# 코드 복사
COPY ./app /app
RUN pip3 install --no-cache-dir fastapi
RUN pip3 install --no-cache-dir mysql-connector-python

EXPOSE 8000

# 환경변수 설정
ENV DB_HOST=tn-sql
ENV DB_USER=admin
ENV DB_PASSWORD=best-student
ENV DB_NAME=tndb

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]