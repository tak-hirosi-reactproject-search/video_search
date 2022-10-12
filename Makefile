UID=
USR=
PORT_NUM=
VIDEO_TARGET_PATH=/home/samchu/project-meta/

SRC_NAME=videoapi
APP_NAME=${SRC_NAME}_${USR}
IMAGE_NAME=${SRC_NAME}_image_${USR}
TARGET_PATH=`pwd`
MODEL_VOLUME = ${TARGET_PATH}:/$(SRC_NAME)

VIDEO_DST_PATH=/videometadata
VIDEO_PATH=${VIDEO_TARGET_PATH}:${VIDEO_DST_PATH}
 
# Build and run the container
build:
	@echo "====<UID=${UID}> <USR=${USR}> <PORT_NUM=${PORT_NUM}> <VIDEO_TARGET_PATH=${VIDEO_TARGET_PATH}>==="
	@echo 'docker image build'
	docker image build --build-arg uid=$(UID) --build-arg gid=$(UID) --build-arg usr=$(USR) --build-arg fname=$(SRC_NAME) --build-arg portnum=$(PORT_NUM) --build-arg datapath=".${VIDEO_TARGET_PATH}" -t $(IMAGE_NAME) .

run:
	@echo 'docker run -tiu --name="$(APP_NAME)" $(IMAGE_NAME)'
	docker run -ti --name "$(APP_NAME)" --shm-size 16gb -p $(PORT_NUM):$(PORT_NUM) -v $(MODEL_VOLUME) -v ${VIDEO_PATH} $(IMAGE_NAME)

stop:
	@echo 'stop docker $(APP_NAME)'
	docker stop $(APP_NAME)

rm:
	@echo 'rm docker $(APP_NAME)'
	docker rm -f $(APP_NAME)

rmi:
	@echo 'rmi docker $(IMAGE_NAME)'
	docker rmi $(IMAGE_NAME)

rmrmi:
	docker stop $(APP_NAME) && docker rm $(APP_NAME)
	docker rmi $(IMAGE_NAME)
