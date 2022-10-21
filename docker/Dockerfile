FROM ubuntu:latest


ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    DEBIAN_FRONTEND=noninteractive \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " 

RUN set -x \
    && sed -i 's@http://archive.ubuntu.com/ubuntu/@http://mirrors.aliyun.com/ubuntu/@g' /etc/apt/sources.list \
    && apt-get update -qq \
    && apt-get upgrade -y \
    && apt-get install -y python3 \
                          python3-dev \
                          python3-pip \
                          libpcre3 \
                          libpcre3-dev \
                          g++ \
                          libmysqlclient-dev \
                          uwsgi-plugin-python3 \
                          libopenblas-dev \
                          liblapack-dev \
                          libatlas-base-dev  \
                          libblas-dev \
                          gfortran  \
                          libpng-dev \
    && apt-get install -y bash \
                        coreutils \
                        moreutils \
                        git \
                        curl \
                        wget \
                        vim \
                        tzdata \
                        perl \
                        openssl \
                        nginx \
                        jq \
                        openssh-server \
                        openssh-client \
                        libffi-dev \
                        make \
                        automake \
                        libcec-dev \
                        libtool \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip config set install.trusted-host mirrors.aliyun.com \
    && apt-get clean -y \
    && apt-get autoclean -y \
    && apt-get update -y \
    && apt-get autoremove -y\
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && git config --global user.email "aptask@@users.noreply.github.com" \
    && git config --global user.name "aptask" \
    && git config --global http.postBuffer 524288000