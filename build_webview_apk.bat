@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   rPPG生理指标检测系统 - APK构建脚本
echo ========================================
echo.

:: 设置错误处理
trap echo 构建过程中断，请检查错误信息 && pause && exit /b 1

:: 检查当前目录
cd /d "%~dp0"
echo 当前工作目录: %CD%
echo.

:: 备份原始main.py
if exist "main.py" (
    echo [1/7] 备份原始main.py...
    copy /Y main.py main_original.py >nul
    if errorlevel 1 (
        echo 警告: 备份失败，继续构建...
    ) else (
        echo 已备份到 main_original.py
    )
)

:: 使用webview版本的main.py
echo [2/7] 切换到WebView版本...
if exist "main_webview.py" (
    copy /Y main_webview.py main.py >nul
    if errorlevel 1 (
        echo 错误: 无法复制main_webview.py
        pause
        exit /b 1
    )
    echo 已切换到WebView版本
) else (
    echo 错误: 未找到main_webview.py文件
    pause
    exit /b 1
)
echo.

:: 检查Python环境
echo [3/7] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        copy /Y main_original.py main.py >nul
    )
    
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set python_version=%%i
echo 检测到: !python_version!
echo.

:: 检查pip
echo [4/7] 检查pip环境...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误: pip不可用
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        copy /Y main_original.py main.py >nul
    )
    
    pause
    exit /b 1
)
echo pip检查通过
echo.

:: 安装依赖
echo [5/7] 安装必要依赖包...
echo 这可能需要几分钟，请耐心等待...
echo.

:: 检查并安装buildozer
python -m pip list | findstr buildozer >nul
if errorlevel 1 (
    echo 正在安装buildozer...
    python -m pip install buildozer --user
    if errorlevel 1 (
        echo 错误: buildozer安装失败
        
        :: 恢复原始main.py
        if exist "main_original.py" (
            copy /Y main_original.py main.py >nul
        )
        
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
        
        :: 恢复原始main.py
        if exist "main_original.py" (
            copy /Y main_original.py main.py >nul
        )
        
        pause
        exit /b 1
    )
    echo kivy安装成功
) else (
    echo kivy已安装
)

echo.

:: 检查必要文件
echo [6/7] 检查项目文件...
if not exist "heart_rate_precision_web.html" (
    echo 错误: 未找到heart_rate_precision_web.html文件
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        copy /Y main_original.py main.py >nul
    )
    
    pause
    exit /b 1
)

if not exist "buildozer.spec" (
    echo 错误: 未找到buildozer.spec文件
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        copy /Y main_original.py main.py >nul
    )
    
    pause
    exit /b 1
)

echo 项目文件检查通过
echo.

:: 开始构建APK
echo [7/7] 开始构建APK文件...
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
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        echo 恢复原始main.py...
        copy /Y main_original.py main.py >nul
    )
    
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo   构建成功！
    echo ========================================
    echo.
    echo APK文件位置：
    echo   %CD%\bin\*.apk
    echo.
    
    :: 恢复原始main.py
    if exist "main_original.py" (
        echo 恢复原始main.py...
        copy /Y main_original.py main.py >nul
        del main_original.py >nul 2>&1
    )
    
    :: 尝试打开输出目录
    if exist "bin" (
        echo 正在打开输出目录...
        start bin
    )
    
    echo.
    echo 下一步操作：
    echo 1. 将APK文件复制到安卓设备
    echo 2. 在设备设置中启用"未知来源"安装
    echo 3. 安装并运行应用
    echo 4. 授权摄像头权限
    echo.
    
    pause
)
