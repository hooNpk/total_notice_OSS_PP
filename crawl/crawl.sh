#!/bin/sh

CUR_DIR=$(pwd)

mkdir /sharespace

IMAGE_NAME="hoonpk/tn-crawl:0.5"
# 이미지가 존재하는지 확인
if docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    echo "이미지 $IMAGE_NAME가 이미 존재합니다."
else
    echo "이미지 $IMAGE_NAME가 존재하지 않습니다. 이미지를 pull합니다."
    docker pull "$IMAGE_NAME"
fi

# 사용자로부터 날짜 입력 받기
echo "크롤링하고 싶은 시작 날짜를 입력하세요 (예: 2024-05-30):"
read start_date
echo "크롤링하고 싶은 종료 날짜를 입력하세요 (예: 2024-05-31):"
read end_date

# 입력이 없을 경우 기본값 설정
start_date=${start_date:-"2024-05-30"}
end_date=${end_date:-"2024-05-31"}

#백그라운드에서 docker container tn-crawl 실행
docker run -d --rm --name tn-crawl --link tn-sql \
    -v $CUR_DIR/sharespace:/sharespace \
    -e START_DATE="$start_date" \
    -e END_DATE="$end_date" \
    "$IMAGE_NAME"

# 테스트용 도커 실행 명령어
# docker run -it --name tn-crawl --link tn-sql \
#     -v $CUR_DIR/sharespace:/sharespace \
#     "$IMAGE_NAME" /bin/bash