#FROM nvcr.io/nvidia/tensorrt:22.05-py3
FROM python:3.8.2
ENV PYTHONBUFFERED 1

SHELL ["/bin/bash", "-c"]

# Setup user account
# id -g, id -u
ARG uid=1014
ARG gid=1014
ARG usr=tglee
RUN groupadd -r -f -g ${gid} ${usr} && useradd -o -r -l -u ${uid} -g ${gid} -ms /bin/bash ${usr}
RUN usermod -aG sudo ${usr}
RUN echo ${usr}:${usr}1 | chpasswd
# RUN mkdir -p /django-react-project && chown ${usr} /django-react-project

# Required to build Ubuntu 20.04 without user prompts with DLFW container
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL ko_KR.UTF-8

# install
RUN apt-get update && apt-get install -y sudo && \
    apt-get install -y libgl1-mesa-glx git locales && \
    locale-gen ko_KR.UTF-8
# RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

# container에 git 설치 & 프로젝트 필요 소스 다운로드
RUN apt-get -qq install curl --yes
RUN apt-get install git --yes

RUN mkdir -p /react-django/video_search && chown ${usr} /react-django/video_search
WORKDIR /react-django/video_search
COPY ./react-django/video_search /react-django/video_search
RUN echo =================`pwd -P`===============
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

USER ${usr}

CMD ["python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
