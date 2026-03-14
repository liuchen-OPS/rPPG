@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   rPPG生理指标检测系统 - Docker构建
echo ========================================
echo.

:: 切换到项目目录
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

:: 创建Dockerfile
echo [2/3] 创建Dockerfile...
(
echo FROM ubuntu:22.04
echo.
echo ENV DEBIAN_FRONTEND=noninteractive
echo ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
echo ENV ANDROIDSDK=/root/.buildozer/android/platform/android-sdk
echo ENV ANDROIDNDK=/root/.buildozer/android/platform/android-ndk-r25b
echo ENV ANDROIDAPI=33
echo ENV ANDROIDMINAPI=21
echo.
echo RUN apt-get update ^&^& apt-get install -y python3 python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libffi-dev libssl-dev automake cmake ^&^& rm -rf /var/lib/apt/lists/*
echo.
echo RUN pip3 install --upgrade pip ^&^& pip3 install buildozer cython kivy
echo.
echo WORKDIR /app
echo.
echo COPY . /app/
.
echo CMD ["buildozer", "-v", "android", "debug"]
) > Dockerfile
echo Dockerfile创建完成
echo.

:: 构建Docker镜像
echo [3/3] 开始构建APK...
echo 注意: 首次构建需要30-60分钟，请耐心等待
echo.

:: 尝试使用不同方式调用docker
where docker >nul 2>&1
if %errorlevel% == 0 (
    echo 使用系统Docker...
    docker build -t rppg-builder . 
    if %errorlevel% == 0 (
        docker run --rm -v "%CD%:/app" rppg-builder
    )
) else (
    echo 尝试使用默认路径...
    "C:\Program Files\Docker\Docker\resources\bin\docker.exe" build -t rppg-builder .
    if %errorlevel% == 0 (
        "C:\Program Files\Docker\Docker\resources\bin\docker.exe" run --rm -v "%CD%:/app" rppg-builder
    )
)

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
    echo 构建失败，请检查Docker是否正确安装并运行
)

:: 恢复原始main.py
if exist "main_original.py" (
    copy /Y main_original.py main.py >nul 2>&1
    del main_original.py >nul 2>&1
)

echo.
pause
