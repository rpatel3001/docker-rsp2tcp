FROM ghcr.io/sdr-enthusiasts/docker-baseimage:soapyrtlsdr

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
    # dependencies for SoapyShared
    KEPT_PACKAGES+=(libsoapysdr-dev) && \
    KEPT_PACKAGES+=(libliquid-dev) && \
    KEPT_PACKAGES+=(libboost-system-dev) && \
    KEPT_PACKAGES+=(libboost-thread-dev) && \
    KEPT_PACKAGES+=(libboost-filesystem-dev) && \
    # Dependencies for SoapyRemote
    KEPT_PACKAGES+=(avahi-daemon) && \
    TEMP_PACKAGES+=(libavahi-client-dev) && \
    KEPT_PACKAGES+=(libavahi-client3) && \
    TEMP_PACKAGES+=(libavahi-common-dev) && \
    KEPT_PACKAGES+=(libavahi-common3) && \
    KEPT_PACKAGES+=(libavahi-common-data) && \
    TEMP_PACKAGES+=(libavahi-core-dev) && \
    KEPT_PACKAGES+=(libavahi-core7) && \
    TEMP_PACKAGES+=(libdbus-1-dev) && \
    KEPT_PACKAGES+=(libdbus-1-3) && \
    # install packages
    apt-get update && \
    apt-get install -y --no-install-recommends \
        "${KEPT_PACKAGES[@]}" \
        "${TEMP_PACKAGES[@]}" && \
    # Deploy SoapyRemote
    git clone https://github.com/pothosware/SoapyRemote.git /src/SoapyRemote && \
    pushd /src/SoapyRemote && \
    BRANCH_SOAPYREMOTE=$(git tag --sort="creatordate" | tail -1) && \
    git checkout "$BRANCH_SOAPYREMOTE" && \
    mkdir -p /src/SoapyRemote/build && \
    pushd /src/SoapyRemote/build && \
    cmake ../ -DCMAKE_BUILD_TYPE=Release && \
    make all && \
    make install && \
    popd && popd && \
    ldconfig && \
    SoapySDRUtil --check=remote && \
    # Deploy SoapyRTLTCP
    git clone https://github.com/pothosware/SoapyRTLTCP.git /src/SoapyRTLTCP && \
    pushd /src/SoapyRTLTCP && \
    mkdir -p /src/SoapyRTLTCP/build && \
    pushd /src/SoapyRTLTCP/build && \
    cmake ../ -DCMAKE_BUILD_TYPE=Release && \
    make all && \
    make install && \
    popd && popd && \
    ldconfig && \
    SoapySDRUtil --check=rtltcp && \
    # Deploy rtlmuxer
    git clone https://github.com/rpatel3001/rtlmuxer.git /src/rtlmuxer && \
    pushd /src/rtlmuxer && \
    make && \
    cp rtlmuxer /usr/local/bin && \
    # Deploy rx_tools
    git clone https://github.com/rxseger/rx_tools.git /src/rx_tools && \
    pushd /src/rx_tools && \
    cmake . && \
    make && \
    cp rx_* /usr/local/bin && \
    # Clean up
    apt-get remove -y "${TEMP_PACKAGES[@]}" && \
    apt-get autoremove -y && \
    rm -rf /src/* /tmp/* /var/lib/apt/lists/*

COPY rootfs/ /
