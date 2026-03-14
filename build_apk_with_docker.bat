@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   rPPG生理指标检测系统 - Docker构建脚本
echo ========================================
echo.

:: 检查Docker
echo [1/5] 检查Docker环境...
docker --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到Docker
    echo.
    echo 请按以下步骤安装Docker Desktop：
    echo 1. 访问 https://www.docker.com/products/docker-desktop/
    echo 2. 下载并安装Docker Desktop for Windows
    echo 3. 启动Docker Desktop并等待其完全启动
    echo 4. 重新运行此脚本
    echo.
    echo 或者使用WSL方案：
    echo   wsl --install -d Ubuntu
    echo.
    start https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('docker --version') do set docker_version=%%i
echo 检测到Docker: !docker_version!
echo.

:: 备份原始main.py
echo [2/5] 备份并切换main.py...
if exist "main.py" (
    copy /Y main.py main_original.py >nul 2>&1
)
if exist "main_webview.py" (
    copy /Y main_webview.py main.py >nul
    echo 已切换到WebView版本
) else (
    echo 警告: 未找到main_webview.py，使用现有main.py
)
echo.

:: 检查文件
echo [3/5] 检查项目文件...
if not exist "heart_rate_precision_web.html" (
    echo 错误: 未找到heart_rate_precision_web.html
    pause
    exit /b 1
)
if not exist "buildozer.spec" (
    echo 错误: 未找到buildozer.spec
    pause
    exit /b 1
)
echo 项目文件检查通过
echo.

:: 创建Dockerfile
echo [4/5] 创建Docker构建环境...
if not exist "Dockerfile" (
    echo 创建Dockerfile...
    (
        echo FROM ubuntu:22.04
        echo.
        echo # 设置环境变量
        echo ENV DEBIAN_FRONTEND=noninteractive
        echo ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
        echo ENV ANDROIDSDK=/root/.buildozer/android/platform/android-sdk
        echo ENV ANDROIDNDK=/root/.buildozer/android/platform/android-ndk-r25b
        echo ENV ANDROIDAPI=33
        echo ENV ANDROIDMINAPI=21
        echo.
        echo # 安装系统依赖
        echo RUN apt-get update ^&^& apt-get install -y \
        echo     python3 python3-pip python3-venv \
        echo     git zip unzip openjdk-17-jdk \
        echo     autoconf libtool pkg-config \
        echo     zlib1g-dev libncurses5-dev libncursesw5-dev \
        echo     libffi-dev libssl-dev \
        echo     automake cmake \
        echo     ^&^& rm -rf /var/lib/apt/lists/*
        echo.
        echo # 安装buildozer和依赖
        echo RUN pip3 install --upgrade pip
        echo RUN pip3 install buildozer cython kivy
        echo.
        echo # 设置工作目录
        echo WORKDIR /app
        echo.
        echo # 复制项目文件
        echo COPY . /app/
        echo.
        echo # 构建APK
        echo CMD ["buildozer", "-v", "android", "debug"]
    ) > Dockerfile
    echo Dockerfile创建成功
) else (
    echo Dockerfile已存在
)
echo.

:: 构建Docker镜像并运行
echo [5/5] 开始构建APK...
echo 注意: 首次构建需要下载大量依赖，可能需要30-60分钟
echo.

:: 构建Docker镜像
echo 构建Docker镜像...
docker build -t rppg-builder .

if errorlevel 1 (
    echo.
    echo 错误: Docker镜像构建失败
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        copy /Y main_original.py main.py >nul 2>&1
        del main_original.py >nul 2>&1
    )
    
    pause
    exit /b 1
)

:: 运行容器构建APK
echo.
echo 开始构建APK...
docker run --rm -v "%CD%:/app" rppg-builder

if errorlevel 1 (
    echo.
    echo ========================================
    echo   构建失败！
    echo ========================================
    echo.
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        copy /Y main_original.py main.py >nul 2>&1
        del main_original.py >nul 2>&1
    )
    
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo   构建成功！
    echo ========================================
    echo.
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        copy /Y main_original.py main.py >nul 2>&1
        del main_original.py >nul 2>&1
    )
    
    :: 检查APK文件
    if exist "bin\*.apk" (
        echo APK文件位置:
        dir /b bin\*.apk
        echo.
        echo 完整路径: %CD%\bin\
    )
    
    echo.
    echo 下一步操作：
    echo 1. 将APK文件复制到安卓设备
    echo 2. 在设备设置中启用'未知来源'安装
    echo 3. 安装并运行应用
    echo.
    
    pause
)
