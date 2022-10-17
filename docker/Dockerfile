FROM python:alpine

ARG AP_MAINTAINER="timiyu"
LABEL maintainer="${AP_MAINTAINER}"
ARG AP_URL=https://github.com/${AP_MAINTAINER}/aptask.git
ARG AP_BRANCH=master

ENV PNPM_HOME=/root/.local/share/pnpm \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.local/share/pnpm:/root/.local/share/pnpm/global/5/node_modules:$PNPM_HOME \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    AP_DIR=/aptask \
    AP_BRANCH=${AP_BRANCH}

WORKDIR ${QL_DIR}

RUN set -x \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk add --update --no-cache py3-configobj \
                                   py3-setuptools \
                                   python3 \
                                   python3-dev \
                                   subversion \
                                   gcc \
                                   g++ \
                                   mariadb-connector-c-dev \
    && apk --no-cache add -f bash \
                             coreutils \
                             moreutils \
                             git \
                             curl \
                             wget \
                             tzdata \
                             perl \
                             openssl \
                             nginx \
                             jq \
                             openssh \
                             libffi-dev \
                             make \
                             automake \
                             jpeg-dev\
                             zlib-dev \
                             libcec-dev \
                             libtool \
    && wget https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py \
    && rm -rf /var/cache/apk/* \
    && apk update \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && git config --global user.email "aptask@@users.noreply.github.com" \
    && git config --global user.name "aptask" \
    && git config --global http.postBuffer 524288000 \
    && git clone -b ${AP_BRANCH} ${AP_URL} ${AP_DIR} \
    && cd ${AP_DIR} \
    && cp -f .env.example .env \
    && chmod 777 ${AP_DIR}/shell/*.sh \
    && chmod 777 ${AP_DIR}/docker/*.sh
    
ENTRYPOINT ["./docker/docker-entrypoint.sh"]
