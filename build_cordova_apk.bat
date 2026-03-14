@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   rPPG生理指标检测系统 - Cordova构建
echo ========================================
echo.

:: 检查Node.js
echo [1/5] 检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Node.js，请先安装Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set node_version=%%i
echo 检测到Node.js: !node_version!
echo.

:: 检查npm
echo [2/5] 检查npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo 错误: npm不可用
    pause
    exit /b 1
)
echo npm检查通过
echo.

:: 安装Cordova
echo [3/5] 安装Cordova...
npm list -g cordova >nul 2>&1
if errorlevel 1 (
    echo 正在安装Cordova...
    npm install -g cordova
    if errorlevel 1 (
        echo 错误: Cordova安装失败
        pause
        exit /b 1
    )
)
echo Cordova已安装
echo.

:: 创建Cordova项目
echo [4/5] 创建Cordova项目...
if not exist "cordova-app" (
    cordova create cordova-app com.example.rppg rPPG生理指标检测系统
    if errorlevel 1 (
        echo 错误: 创建Cordova项目失败
        pause
        exit /b 1
    )
)

:: 复制HTML文件到Cordova项目
echo 复制HTML文件...
copy /Y heart_rate_precision_web.html cordova-app\www\index.html >nul
if errorlevel 1 (
    echo 错误: 复制HTML文件失败
    pause
    exit /b 1
)

:: 修改Cordova配置
echo 配置Cordova...
cd cordova-app

:: 添加Android平台
echo [5/5] 添加Android平台...
cordova platform add android
if errorlevel 1 (
    echo 警告: Android平台可能已存在，继续构建...
)

:: 构建APK
echo.
echo 开始构建APK...
cordova build android

if errorlevel 1 (
    echo.
    echo ========================================
    echo   构建失败！
    echo ========================================
    echo.
    cd ..
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo   构建成功！
    echo ========================================
    echo.
    echo APK文件位置：
    echo   %CD%\platforms\android\app\build\outputs\apk\debug\app-debug.apk
    echo.
    
    :: 复制APK到根目录
    copy platforms\android\app\build\outputs\apk\debug\app-debug.apk ..\rPPG生理指标检测系统.apk >nul 2>&1
    
    cd ..
    
    echo APK已复制到: rPPG生理指标检测系统.apk
    echo.
    echo 下一步操作：
    echo 1. 将APK文件复制到安卓设备
    echo 2. 在设备设置中启用"未知来源"安装
    echo 3. 安装并运行应用
    echo.
    
    pause
)
