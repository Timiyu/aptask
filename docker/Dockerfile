FROM alpine:latest

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " 

RUN set -x \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk add --update --no-cache py3-configobj \
                                   py3-setuptools \
                                   python3 \
                                   python3-dev \
                                   subversion \
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
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/cache/apk/* \
    && apk update \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && git config --global user.email "aptask@@users.noreply.github.com" \
    && git config --global user.name "aptask" \
    && git config --global http.postBuffer 524288000
