@echo off
chcp 65001 >nul
echo ========================================
echo 科学级rPPG心率检测系统
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查并安装依赖
echo [1/3] 检查依赖...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

echo [2/3] 安装依赖...
call venv\Scripts\activate
pip install -r requirements.txt -q

echo [3/3] 启动服务器...
echo.
echo ========================================
echo 访问地址: http://localhost:5000
echo 按Ctrl+C停止服务器
echo ========================================
echo.

python app.py

pause
