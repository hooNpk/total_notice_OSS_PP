#!/bin/sh

CUR_DIR=$(pwd)

mkdir /sharespace

IMAGE_NAME="hoonpk/tn-crawl:0.2"
# 이미지가 존재하는지 확인
if docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    echo "이미지 $IMAGE_NAME가 이미 존재합니다."
else
    echo "이미지 $IMAGE_NAME가 존재하지 않습니다. 이미지를 pull합니다."
    docker pull "$IMAGE_NAME"
fi

#백그라운드에서 docker container tn-crawl 실행
docker run -d --rm --name tn-crawl --link tn-sql -v $CUR_DIR/sharespace:/sharespace hoonpk/tn-crawl:0.2
