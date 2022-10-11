
# Video Search
using (react - django RESTapi ) study project!


# how to install (source)
```bash
git clone https://github.com/tak-hirosi-reactproject-search/video_search.git
cd video_search
```

# 가상환경 세팅
pip를 실행할 수 있는 환경

### how to set env
```bash
pip install -r requirements.txt
```

### how to run server
```bash
python manage.py runserver 0.0.0.0:3355
```

# docker 세팅
docker를 실행할 수 있는 환경


### Please Set Makefile
```Makefile
UID={#Change}
USR={#Change}
PORT_NUM={#Change}
VIDEO_TARGET_PATH=/home/samchu/project-meta/
```

### how to make docker
```bash
make build
```

### how to server run (for docker)
```bash
make run
```

### how to delete container (for docker)
```bash
make rm
```
