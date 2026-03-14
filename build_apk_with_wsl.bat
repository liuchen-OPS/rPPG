@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   rPPG生理指标检测系统 - WSL构建脚本
echo ========================================
echo.

:: 检查WSL
echo [1/5] 检查WSL环境...
wsl --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到WSL，请先安装WSL
    echo 安装命令: wsl --install
    pause
    exit /b 1
)
echo WSL已安装
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

:: 复制文件到WSL
echo [4/5] 准备WSL环境...
echo 将项目文件复制到WSL...

:: 创建WSL中的构建目录
wsl mkdir -p ~/rppg-build

:: 复制所有必要文件到WSL
wsl cp -r /mnt/d/rPPG安卓化/* ~/rppg-build/ 2>nul || (
    echo 使用PowerShell复制文件...
    powershell -Command "Copy-Item -Path 'D:\rPPG安卓化\*' -Destination '\\wsl$\Ubuntu\home\%USERNAME%\rppg-build\' -Recurse -Force"
)

echo 文件复制完成
echo.

:: 在WSL中安装依赖并构建
echo [5/5] 在WSL中构建APK...
echo 注意: 首次构建需要下载大量依赖，可能需要30-60分钟
echo.

wsl bash -c "
cd ~/rppg-build
echo '更新包列表...'
sudo apt-get update -qq

echo '安装Python和依赖...'
sudo apt-get install -y -qq python3 python3-pip python3-venv git zip unzip openjdk-17-jdk

echo '创建虚拟环境...'
python3 -m venv venv
source venv/bin/activate

echo '安装buildozer和依赖...'
pip install -q buildozer cython

echo '开始构建APK...'
buildozer -v android debug

if [ \$? -eq 0 ]; then
    echo '构建成功！'
    echo '复制APK到Windows...'
    cp bin/*.apk /mnt/d/rPPG安卓化/ 2>/dev/null || true
else
    echo '构建失败，请检查错误信息'
    exit 1
fi
"

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
