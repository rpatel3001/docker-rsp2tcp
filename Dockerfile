FROM ghcr.io/sdr-enthusiasts/docker-baseimage:python

ENV TCP_PORT=7374

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# hadolint ignore=DL3008,SC2086,DL4006,SC2039
RUN set -x && \
    TEMP_PACKAGES=() && \
    KEPT_PACKAGES=() && \
    # packages needed to install
    TEMP_PACKAGES+=(git) && \
    # packages needed for my sanity
    KEPT_PACKAGES+=(nano) && \
    # packages needed to build
    TEMP_PACKAGES+=(build-essential) && \
    TEMP_PACKAGES+=(cmake) && \
    TEMP_PACKAGES+=(pkg-config) && \
    # packages needed for SDRplay driver
    TEMP_PACKAGES+=(libusb-1.0-0-dev) && \
    KEPT_PACKAGES+=(libusb-1.0-0) && \
    # install packages
    apt-get update && \
    apt-get install -y --no-install-recommends \
        "${KEPT_PACKAGES[@]}" \
        "${TEMP_PACKAGES[@]}"

COPY sdrplay/ /src/sdrplay/

# hadolint ignore=DL3008,SC2086,DL4006,SC2039
RUN set -x && \
    # Deploy rtlmuxer
    git clone https://github.com/rpatel3001/rtlmuxer.git /src/rtlmuxer && \
    pushd /src/rtlmuxer && \
    make && \
    cp rtlmuxer /usr/local/bin && \
    popd && \
    # install SDRPlay driver
    mkdir -p /etc/udev/rules.d && \
    pushd /src/sdrplay && \
    chmod +x install.sh && \
    ./install.sh && \
    popd && \
    # install SDRplay TCP server
    git clone https://github.com/SDRplay/RSPTCPServer.git /src/sdrplay/rsp_tcp && \
    pushd /src/sdrplay/rsp_tcp && \
    patch --verbose -N < ../rsp_tcp.patch && \
    sed -i "s#\([^f]\)printf(#\1fprintf(stderr, #" rsp_tcp.c && \
    mkdir build && \
    pushd build && \
    cmake .. && \
    make && \
    make install && \
    popd && popd && \
    # Clean up
    apt-get remove -y "${TEMP_PACKAGES[@]}" && \
    apt-get autoremove -y && \
    rm -rf /src/* /tmp/* /var/lib/apt/lists/*

COPY rootfs/ /
