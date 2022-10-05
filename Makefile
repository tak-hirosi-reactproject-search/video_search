UID=1014
USR=tglee
APP_NAME=video_search
IMAGE_NAME=video_search_image
MODEL_VOLUME = /home/${USR}/react-django/$(APP_NAME):/$(APP_NAME)
 
# Build and run the container
build:
	@echo "docker image build --build-arg uid=$(UID) --build-arg gid=$(UID) --build-arg usr=$(USR) -t $(IMAGE_NAME) ."
	docker image build --build-arg uid="$(UID)" --build-arg gid="$(UID)" --build-arg usr="$(USR)" -t $(IMAGE_NAME) .
run:
	@echo 'docker run -ti --name="$(APP_NAME)" --shm-size 32gb -v $(MODEL_VOLUME) $(IMAGE_NAME)'
	# docker run -d -t --name="$(APP_NAME)" --net=host --ipc=host --shm-size 32gb -v $(MODEL_VOLUME) $(IMAGE_NAME)
	docker run -ti --name="$(APP_NAME)" --shm-size 32gb -v $(MODEL_VOLUME) $(IMAGE_NAME)
stop:
	@echo 'stop docker $(APP_NAME)'
	docker stop $(APP_NAME)
rm:
	@echo 'rm docker $(APP_NAME)'
	docker rm -f $(APP_NAME)
rmi:
	@echo 'rmi docker $(IMAGE_NAME)'
	docker rmi $(IMAGE_NAME)
