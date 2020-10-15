FROM docker.io/bitnami/minideb:buster

ENV HOME="/" \
    OS_ARCH="amd64" \
    OS_FLAVOUR="debian-10" \
    OS_NAME="linux"

COPY meminstlpack/prebuildfs /
# Install required system packages and dependencies
RUN install_packages acl ca-certificates curl gzip libc6 libevent-2.1-6 libsasl2-2 libsasl2-modules procps sasl2-bin tar
RUN . /opt/bitnami/scripts/libcomponent.sh && component_unpack "memcached" "1.6.7-0" --checksum 736b53ed71e0af83e178c54e7427fba85b36feca5ec6d70ec8ade3cf63acab81
RUN . /opt/bitnami/scripts/libcomponent.sh && component_unpack "gosu" "1.12.0-1" --checksum 51cfb1b7fd7b05b8abd1df0278c698103a9b1a4964bdacd87ca1d5c01631d59c
RUN apt-get update && apt-get upgrade -y && \
    rm -r /var/lib/apt/lists /var/cache/apt/archives
RUN chmod g+rwX /opt/bitnami
RUN ln -s /opt/bitnami/scripts/memcached/entrypoint.sh /entrypoint.sh
RUN ln -s /opt/bitnami/scripts/memcached/run.sh /run.sh


COPY meminstlpack/rootfs /
RUN /opt/bitnami/scripts/memcached/postunpack.sh

RUN install_packages build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libcrypto++-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev libsqlite3-dev libffi-dev

RUN curl -O https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tar.xz

RUN tar -xf Python-3.7.7.tar.xz

WORKDIR Python-3.7.7

RUN ./configure --enable-loadable-sqlite-extensions --enable-optimizations
RUN make

RUN make install

ENV BITNAMI_APP_NAME="memcached" \
    BITNAMI_IMAGE_VERSION="1.6.7-debian-10-r9" \
    PATH="/opt/bitnami/memcached/bin:/opt/bitnami/common/bin:$PATH"

EXPOSE 11211



RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN chown 1121 /usr/src/app/
RUN chmod 666 Cache/files/categories.json
RUN chmod 666 Cache/files/coords.pickle
RUN chmod 666 Cache/files/index_cache.p
RUN chmod 666 Cache/files/locality.pickle
RUN chmod 666 Cache/files/regions.pickle
RUN chmod 666 Cache/files/stopwords.txt
RUN chmod 666 Cache/files/struct_actual_vac.pickle
RUN chmod 666 Cache/files/token.pickle
RUN chmod 666 vac_bot_logs.log


RUN python3 -m pip install -r requirements.txt
# RUN python3 -m pip install -i http://mirror.whatever/pypi/simple --trusted-host mirror.whatever --user -r requirements.txt
# RUN python3 -m pip install --index-url http://mirror.sigma.sbrf.ru/pypi/simple --trusted-host mirror.sigma.sbrf.ru -r requirements.txt
USER 1121
ENTRYPOINT ["/bin/bash"]
CMD ["run.sh"]