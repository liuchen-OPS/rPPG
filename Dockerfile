FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
ENV ANDROIDSDK=/root/.buildozer/android/platform/android-sdk
ENV ANDROIDNDK=/root/.buildozer/android/platform/android-ndk-r25b
ENV ANDROIDAPI=33
ENV ANDROIDMINAPI=21

RUN apt-get update && apt-get install -y python3 python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libffi-dev libssl-dev automake cmake && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && pip3 install buildozer cython kivy

WORKDIR /app

COPY . /app/

CMD ["buildozer", "-v", "android", "debug"]
