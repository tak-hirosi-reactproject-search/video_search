FROM ubuntu:latest-alpine

SHELL ["/bin/bash", "-c"]

# Setup user account
# id -g, id -u
ARG uid=1014
ARG gid=${uid}
ARG usr=tglee
RUN groupadd -r -f -g ${gid} ${usr} && useradd -o -r -l -u ${uid} -g ${gid} -ms /bin/bash ${usr}
RUN usermod -aG sudo ${usr}
RUN echo ${usr}:${usr}1 | chpasswd
# RUN mkdir -p /django-react-project && chown ${usr} /django-react-project

# Required to build Ubuntu 20.04 without user prompts with DLFW container
ENV DEBIAN_FRONTEND=noninteractive

# install
RUN apt-get update && apt-get install -y sudo \
    && apt-get install -y libgl1-mesa-glx git locales \
    && apt-get install -y locales curl python3. 8 - distutils \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && pip install -U pip \
    && mkdir /code \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen ko_KR.UTF-8
# RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116


# 프로젝트 필요 소스 다운로드
ENV LC_ALL ko_KR.UTF-8

RUN mkdir -p /react-django/video_search && chown ${usr} /react-django/video_search
WORKDIR /react-django/video_search
COPY . .
# RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# EXPOSE 8000

USER ${usr}
RUN ["/bin/bash"]
