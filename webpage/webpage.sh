# Run backend
BACK_IMAGE_NAME="hoonpk/tn-back:0.2"
# 이미지가 존재하는지 확인
if docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    echo "이미지 $IMAGE_NAME가 이미 존재합니다."
else
    echo "이미지 $IMAGE_NAME가 존재하지 않습니다. 이미지를 pull합니다."
    docker pull "$IMAGE_NAME"
fi

docker run -d --rm --name tn-back \
    --link tn-sql \
    -p 8000:8000 \
    "$BACK_IMAGE_NAME"


# Run frontend
FRONT_IMAGE_NAME="hoonpk/tn-front:0.3"
# 이미지가 존재하는지 확인
if docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    echo "이미지 $IMAGE_NAME가 이미 존재합니다."
else
    echo "이미지 $IMAGE_NAME가 존재하지 않습니다. 이미지를 pull합니다."
    docker pull "$IMAGE_NAME"
fi

docker run -d --rm --name tn-front -p 80:80 "$FRONT_IMAGE_NAME"
