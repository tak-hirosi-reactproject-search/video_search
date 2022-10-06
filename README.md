
# Video Search
using (react - django RESTapi ) study project!

# 세팅
docker를 실행할 수 있는 환경


# how to install (source & docker container)
```bash
git clone https://github.com/tak-hirosi-reactproject-search/video_search.git
cd video_search

```

# Please Set Makefile
```Makefile
UID=1014 {# change }
USR=tglee {# change }
APP_NAME=videoapi
IMAGE_NAME= {# change }
TARGET_PATH={# change }/video_search
```

# how to make docker
```bash
make build
```

# how to server run
```bash
make run
```

# how to delete container
```bash
make rm
```
