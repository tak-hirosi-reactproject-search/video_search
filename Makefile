UID=1014
USR=tglee
APP_NAME=video_search
IMAGE_NAME=video_search_image
MODEL_VOLUME = /home/${USR}/react-django/$(APP_NAME):/react-django/$(APP_NAME)
 
# Build and run the container
build:
	@echo 'build docker $(APP_NAME)'
	@echo "docker image build --build-arg uid=$(UID) --build-arg usr=$(USR) -t $(APP_NAME) ."
  	# docker image build --build-arg uid="$(UID)" --build-arg usr="$(USR)" -t $(APP_NAME) .
run:
	@echo 'run docker $(APP_NAME)'
	#docker run -d -t --name="$(APP_NAME)" --net=host --ipc=host --shm-size 32gb -v $(MODEL_VOLUME) $(IMAGE_NAME)
	docker run -ti --name="$(APP_NAME)" --net=host --ipc=host --shm-size 32gb -v $(MODEL_VOLUME) $(IMAGE_NAME)
stop:
	@echo 'stop docker $(APP_NAME)'
	docker stop $(APP_NAME)
rm:
	@echo 'rm docker $(APP_NAME)'
	docker rm -f $(APP_NAME)
rmi:
	@echo 'rmi docker $(APP_NAME)'
	docker rmi $(APP_NAME)
