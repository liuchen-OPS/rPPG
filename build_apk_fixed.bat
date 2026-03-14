@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   心率检测安卓应用构建脚本（修复版）
echo ========================================
echo.

:: 设置错误处理
trap echo 构建过程中断，请检查错误信息 && pause && exit /b 1

:: 检查当前目录
cd /d "%~dp0"
echo 当前工作目录: %CD%
echo.

:: 步骤1: 检查Python环境
echo [1/6] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set python_version=%%i
echo 检测到: !python_version!
echo.

:: 步骤2: 检查pip是否可用
echo [2/6] 检查pip环境...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误: pip不可用，请重新安装Python
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python -m pip --version') do set pip_version=%%i
echo 检测到: !pip_version!
echo.

:: 步骤3: 安装必要依赖
echo [3/6] 安装必要依赖包...
echo 这可能需要几分钟，请耐心等待...
echo.

:: 检查并安装buildozer
python -m pip list | findstr buildozer >nul
if errorlevel 1 (
    echo 正在安装buildozer...
    python -m pip install buildozer --user
    if errorlevel 1 (
        echo 错误: buildozer安装失败
        echo 尝试使用管理员权限运行此脚本
        pause
        exit /b 1
    )
    echo buildozer安装成功
) else (
    echo buildozer已安装
)

:: 检查并安装kivy
python -m pip list | findstr kivy >nul
if errorlevel 1 (
    echo 正在安装kivy...
    python -m pip install kivy --user
    if errorlevel 1 (
        echo 错误: kivy安装失败
        pause
        exit /b 1
    )
    echo kivy安装成功
) else (
    echo kivy已安装
)

:: 检查并安装numpy
python -m pip list | findstr numpy >nul
if errorlevel 1 (
    echo 正在安装numpy...
    python -m pip install numpy --user
    if errorlevel 1 (
        echo 错误: numpy安装失败
        pause
        exit /b 1
    )
    echo numpy安装成功
) else (
    echo numpy已安装
)

echo.

:: 步骤4: 检查必要文件
echo [4/6] 检查项目文件...
if not exist "main.py" (
    echo 错误: 未找到main.py文件
    pause
    exit /b 1
)

if not exist "buildozer.spec" (
    echo 错误: 未找到buildozer.spec文件
    pause
    exit /b 1
)

echo 项目文件检查通过
echo.

:: 步骤5: 初始化Buildozer（如果需要）
echo [5/6] 初始化Buildozer环境...
if not exist ".buildozer" (
    echo 首次运行，正在初始化Buildozer...
    python -m buildozer init
    if errorlevel 1 (
        echo 警告: Buildozer初始化可能有问题，但继续构建...
    )
) else (
    echo Buildozer环境已存在
)

echo.

:: 步骤6: 开始构建APK
echo [6/6] 开始构建APK文件...
echo 注意: 首次构建需要下载Android SDK/NDK，可能需要30-60分钟
echo 请确保网络连接稳定，不要中断此过程
echo.
echo 构建日志将显示在下方...
echo ========================================
echo.

:: 设置构建选项
set BUILDOPTS=-v

:: 开始构建
python -m buildozer %BUILDOPTS% android debug

:: 检查构建结果
if errorlevel 1 (
    echo.
    echo ========================================
    echo   构建失败！
    echo   可能的原因：
    echo   - 网络连接问题
    echo   - 磁盘空间不足
    echo   - 系统权限问题
    echo   - 依赖包冲突
    echo ========================================
    echo.
    echo 建议解决方案：
    echo 1. 检查网络连接
    echo 2. 确保C盘有足够空间（至少5GB）
    echo 3. 以管理员身份运行此脚本
    echo 4. 查看.buildozer目录下的详细日志
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo   构建成功！��
    echo ========================================
    echo.
    echo APK文件位置：
    echo   %CD%\bin\heartrateapp-0.1-debug.apk
    echo.
    echo 下一步操作：
    echo 1. 将APK文件复制到安卓设备
    echo 2. 在设备设置中启用"未知来源"安装
    echo 3. 安装并运行应用
    echo 4. 授权摄像头权限
    echo.
    
    :: 尝试打开输出目录
    if exist "bin" (
        echo 正在打开输出目录...
        start bin
    )
    
