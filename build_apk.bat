@echo off
echo ========================================
echo   心率检测安卓应用构建脚本
echo ========================================
echo.

echo 步骤1: 检查Python环境
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo.
echo 步骤2: 检查Buildozer是否安装
pip list | findstr buildozer
if errorlevel 1 (
    echo Buildozer未安装，正在安装...
    pip install buildozer
    if errorlevel 1 (
        echo 错误: Buildozer安装失败
        pause
        exit /b 1
    )
)

echo.
echo 步骤3: 检查Kivy是否安装
pip list | findstr kivy
if errorlevel 1 (
    echo Kivy未安装，正在安装...
    pip install kivy
    if errorlevel 1 (
        echo 错误: Kivy安装失败
        pause
        exit /b 1
    )
)

echo.
echo 步骤4: 初始化Buildozer
buildozer init
if errorlevel 1 (
    echo 错误: Buildozer初始化失败
    pause
    exit /b 1
)

echo.
echo 步骤5: 开始构建APK（这可能需要较长时间）
echo 注意: 首次构建需要下载Android SDK/NDK，请确保网络连接稳定
echo.
buildozer -v android debug

if errorlevel 1 (
    echo.
    echo ========================================
    echo   构建失败，请检查错误信息
    echo ========================================
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo   构建成功！APK文件位置:
    echo   d:\rPPG安卓化\bin\heartrateapp-0.1-debug.apk
    echo ========================================
    pause
)