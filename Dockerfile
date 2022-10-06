FROM nvcr.io/nvidia/tensorrt:22.05-py3

SHELL ["/bin/bash", "-c"]

# Setup user account
# id -g, id -u
ARG uid
ARG gid
ARG usr
ARG fname
ARG portnum

# Required to build Ubuntu 20.04 without user prompts with DLFW container
ENV DEBIAN_FRONTEND=noninteractive
ENV Portnum=0.0.0.0:${portnum}

# install
RUN apt-get update && apt-get install -y sudo \
    && apt-get install -y libgl1-mesa-glx git locales \
    && locale-gen ko_KR.UTF-8
# RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

# 프로젝트 필요 소스 다운로드
ENV LC_ALL ko_KR.UTF-8
RUN pip install --upgrade pip
RUN mkdir -p /${fname}
WORKDIR /${fname}
COPY . .
# RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN echo 'python manage.py runserver ${Portnum}'
RUN ["/bin/bash"]
CMD ["python", "manage.py", "runserver", "$Portnum"]
