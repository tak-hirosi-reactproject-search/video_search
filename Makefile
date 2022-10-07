UID=1006
USR=jhlee
APP_NAME=videoapi
IMAGE_NAME=videoapi_image
TARGET_PATH=/home/${USR}/workspace/helloworld/search_module
MODEL_VOLUME = ${TARGET_PATH}:/$(APP_NAME)
PORT_NUM=3333
VIDEO_PATH=/home/samchu/project-meta/output_metadata/
 
# Build and run the container
build:
	@cp -r ${VIDEO_PATH} ./temps
	docker image build --build-arg uid=$(UID) --build-arg gid=$(UID) --build-arg usr=$(USR) --build-arg fname=$(APP_NAME) --build-arg portnum=$(PORT_NUM) --build-arg datapath="./temps" -t $(IMAGE_NAME) .

run:
	@echo 'docker run -ti --name="$(APP_NAME)_$(USR)" --shm-size 32gb -p $(PORT_NUM):$(PORT_NUM) -v $(MODEL_VOLUME) $(IMAGE_NAME)'
	docker run -ti --name="$(APP_NAME)_$(USR)" --shm-size 16gb -p $(PORT_NUM):$(PORT_NUM) -v $(MODEL_VOLUME) $(IMAGE_NAME)

stop:
	@echo 'stop docker $(APP_NAME)_$(USR)'
	docker stop $(APP_NAME)_$(USR)

rm:
	@echo 'rm docker $(APP_NAME)_$(USR)'
	docker rm -f $(APP_NAME)_$(USR)

rmi:
	@echo 'rmi docker $(IMAGE_NAME)'
	docker rmi $(IMAGE_NAME)

rmrmi:
	docker stop $(APP_NAME)_$(USR) && docker rm $(APP_NAME)_$(USR)
	docker rmi $(IMAGE_NAME)
