# Run backend
BACK_IMAGE_NAME="hoonpk/tn-back:0.3"
# 이미지가 존재하는지 확인
if docker image inspect "$BACK_IMAGE_NAME" > /dev/null 2>&1; then
    echo "이미지 $BACK_IMAGE_NAME 이미 존재합니다."
else
    echo "이미지 $BACK_IMAGE_NAME 존재하지 않습니다. 이미지를 pull합니다."
    docker pull "$BACK_IMAGE_NAME"
fi

docker run -d --rm --name tn-back \
    --link tn-sql \
    -p 8000:8000 \
    "$BACK_IMAGE_NAME"


# Run frontend
FRONT_IMAGE_NAME="hoonpk/tn-front:0.4"
# 이미지가 존재하는지 확인
if docker image inspect "$FRONT_IMAGE_NAME" > /dev/null 2>&1; then
    echo "이미지 $FRONT_IMAGE_NAME 이미 존재합니다."
else
    echo "이미지 $FRONT_IMAGE_NAME 존재하지 않습니다. 이미지를 pull합니다."
    docker pull "$FRONT_IMAGE_NAME"
fi

docker run -d --rm --name tn-front -p 80:80 "$FRONT_IMAGE_NAME"
