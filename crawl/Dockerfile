
#TODO 시작일자와 종료일자를 매개변수로 받아야 함
FROM python:3.10
RUN apt-get update
RUN pip3 install --no-cache-dir pandas
RUN pip3 install --no-cache-dir beautifulsoup4
RUN pip3 install --no-cache-dir requests

RUN mkdir /workspace/
RUN mkdir /sharespace/
COPY main.py /workspace/main.py

ARG START_DATE="2024-05-30"
ARG END_DATE="2024-05-31"

#ENTRYPOINT ["python"]
#CMD ["/workspace/main.py", $START_DATE, $END_DATE]
CMD ["python", "/workspace/main.py"]