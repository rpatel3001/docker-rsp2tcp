#!/bin/bash

ARCH=$(uname -m)

case $ARCH in
  x86_64)
    BINARY=SDRplay_RSP_API-Linux-3.07.1.run
    ;;
  armv*)
    BINARY=SDRplay_RSP_API-ARM32-3.07.2.run
    ARCH=armv7l
    ;;
  aarch64)
    BINARY=SDRplay_RSP_API-ARM64-3.07.1.run
    ;;
esac

sh $BINARY --noexec --target sdrplay
patch --verbose -Np0 < ./install-lib.$ARCH.patch

cd sdrplay
sed -i "s#sudo ##" install_lib.sh
./install_lib.sh
cd ..