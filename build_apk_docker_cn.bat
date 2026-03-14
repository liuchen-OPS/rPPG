@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   rPPG生理指标检测系统 - Docker构建(国内镜像)
echo ========================================
echo.

cd /d "%~dp0"

:: 备份并切换main.py
echo [1/3] 准备构建环境...
if exist "main.py" (
    copy /Y main.py main_original.py >nul 2>&1
)
if exist "main_webview.py" (
    copy /Y main_webview.py main.py >nul
    echo 已切换到WebView版本
)
echo.

:: 创建Dockerfile使用国内镜像
echo [2/3] 创建Dockerfile(使用阿里云镜像)...
(
echo FROM registry.cn-hangzhou.aliyuncs.com/library/ubuntu:22.04
echo.
echo ENV DEBIAN_FRONTEND=noninteractive
echo ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
echo ENV ANDROIDSDK=/root/.buildozer/android/platform/android-sdk
echo ENV ANDROIDNDK=/root/.buildozer/android/platform/android-ndk-r25b
echo ENV ANDROIDAPI=33
echo ENV ANDROIDMINAPI=21
echo.
echo RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list ^&^& sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
echo.
echo RUN apt-get update ^&^& apt-get install -y python3 python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libffi-dev libssl-dev automake cmake ^&^& rm -rf /var/lib/apt/lists/*
echo.
echo RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple ^&^& pip3 install buildozer cython kivy -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo WORKDIR /app
echo.
echo COPY . /app/
echo.
echo CMD ["buildozer", "-v", "android", "debug"]
) > Dockerfile
echo Dockerfile创建完成
echo.

:: 构建Docker镜像
echo [3/3] 开始构建APK...
echo 注意: 首次构建需要30-60分钟，请耐心等待
echo.

docker build -t rppg-builder .
if %errorlevel% == 0 (
    echo.
    echo Docker镜像构建成功，开始构建APK...
    docker run --rm -v "%CD%:/app" rppg-builder
    
    if %errorlevel% == 0 (
        echo.
        echo ========================================
        echo   构建成功！
        echo ========================================
        echo.
        if exist "bin\*.apk" (
            echo APK文件:
            dir /b bin\*.apk
        )
    ) else (
        echo.
        echo APK构建失败
    )
) else (
    echo.
    echo Docker镜像构建失败
    echo.
    echo 可能的解决方案:
    echo 1. 检查网络连接
    echo 2. 配置Docker使用代理
    echo 3. 尝试使用WSL方案: wsl --install -d Ubuntu
    echo 4. 使用GitHub Actions在线构建
)

:: 恢复原始main.py
if exist "main_original.py" (
    copy /Y main_original.py main.py >nul 2>&1
    del main_original.py >nul 2>&1
)

echo.
pause
