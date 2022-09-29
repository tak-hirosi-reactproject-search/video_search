USR=tglee
APP_NAME=video_search_tg
MODEL_VOLUME = /home/${USR}/react-django/$(APP_NAME):/react-django/$(APP_NAME)
 
# Build and run the container
build:
	@echo 'build docker $(APP_NAME)'
  	docker image build -t  .

run:
	@echo 'run docker $(APP_NAME)'
	docker run -d -t --name="$(APP_NAME)" --net=host --ipc=host --shm-size 16gb -v $(MODEL_VOLUME)

stop:
	@echo 'stop docker $(APP_NAME)'
	docker stop $(APP_NAME)

rm:
	@echo 'rm docker $(APP_NAME)'
	docker rm -f $(APP_NAME)

rmi:
	@echo 'rmi docker $(APP_NAME)'
	docker rmi $(APP_NAME)
