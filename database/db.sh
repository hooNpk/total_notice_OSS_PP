#!/bin/sh

IMAGE_NAME="hoonpk/tn-sql:0.1"

# 이미지가 존재하는지 확인
if docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    echo "이미지 $IMAGE_NAME가 이미 존재합니다."
else
    echo "이미지 $IMAGE_NAME가 존재하지 않습니다. 이미지를 pull합니다."
    docker pull "$IMAGE_NAME"
fi

docker run --name tn-sql -d -p 3306:3306 $IMAGE_NAME