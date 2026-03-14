@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   构建环境诊断工具
echo ========================================
echo.

:: 记录开始时间
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do set datetime=%%i
set start_time=!datetime!

echo 诊断开始时间: !start_time!
echo.

:: 1. 系统信息
echo [1/8] 系统信息检查...
echo 操作系统:
ver
echo.

:: 2. 磁盘空间检查
echo [2/8] 磁盘空间检查...
for /f "tokens=1-3" %%a in ('dir /-c ^| find "字节可用"') do set free_space=%%c
echo C盘可用空间: !free_space!
if !free_space! LSS 5000000000 (
    echo 警告: 磁盘空间可能不足，建议清理至少5GB空间
) else (
    echo 磁盘空间充足
)
echo.

:: 3. Python环境检查
echo [3/8] Python环境检查...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    goto python_error
) else (
    for /f "tokens=*" %%i in ('python --version') do set python_ver=%%i
    echo ✅ !python_ver!
)

python -c "import sys; print('Python路径:', sys.executable)"
if errorlevel 1 (
    echo ❌ Python执行异常
    goto python_error
)
echo.

:: 4. PIP环境检查
echo [4/8] PIP环境检查...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ PIP不可用
    goto pip_error
) else (
    for /f "tokens=*" %%i in ('python -m pip --version') do set pip_ver=%%i
    echo ✅ !pip_ver!
)
echo.

:: 5. 必要包检查
echo [5/8] 必要包检查...
set packages=buildozer kivy numpy

for %%p in (%packages%) do (
    python -m pip show %%p >nul 2>&1
    if errorlevel 1 (
        echo ❌ %%p 未安装
        set missing_packages=!missing_packages! %%p
    ) else (
        echo ✅ %%p 已安装
    )
)

if defined missing_packages (
    echo.
    echo 缺失的包: !missing_packages!
    echo 运行 build_apk_fixed.bat 自动安装
) else (
    echo ✅ 所有必要包都已安装
)
echo.

:: 6. 项目文件检查
echo [6/8] 项目文件检查...
set required_files=main.py buildozer.spec
set missing_files=

for %%f in (%required_files%) do (
    if exist "%%f" (
        echo ✅ %%f 存在
    ) else (
        echo ❌ %%f 缺失
        set missing_files=!missing_files! %%f
    )
)

if defined missing_files (
    echo.
    echo 错误: 以下文件缺失: !missing_files!
    goto file_error
) else (
    echo ✅ 所有必要文件都存在
)
echo.

:: 7. Buildozer环境检查
echo [7/8] Buildozer环境检查...
if exist ".buildozer" (
    echo ✅ Buildozer环境已初始化
    dir .buildozer /b
) else (
    echo ⚠️ Buildozer环境未初始化
    echo 首次运行 build_apk_fixed.bat 时会自动初始化
)
echo.

:: 8. 网络连接检查
echo [8/8] 网络连接检查...
ping -n 1 www.google.com >nul 2>&1
if errorlevel 1 (
    ping -n 1 www.baidu.com >nul 2>&1
    if errorlevel 1 (
        echo ⚠️ 网络连接可能有问题
        echo 构建过程需要稳定的网络连接
    ) else (
        echo ✅ 网络连接正常
    )
) else (
    echo ✅ 网络连接正常
)

echo.
echo ========================================
echo   诊断完成
echo ========================================
echo.
echo 建议操作:
if defined missing_packages (
    echo 1. 运行 build_apk_fixed.bat 安装缺失的包
) else (
    echo 1. 所有环境检查通过，可以开始构建
)

echo 2. 确保有稳定的网络连接
echo 3. 确保C盘有足够空间（建议5GB以上）
echo 4. 首次构建可能需要30-60分钟
echo.

:: 记录结束时间
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do set datetime=%%i
set end_time=!datetime!
echo 诊断结束时间: !end_time!

echo.
pause
goto end

:python_error
echo.
echo ========================================
echo   Python环境问题
echo ========================================
echo.
echo 解决方案:
echo 1. 下载并安装Python 3.7+: https://www.python.org/downloads/
echo 2. 安装时勾选"Add Python to PATH"
echo 3. 重新启动命令提示符
echo.
pause
goto end

:pip_error
echo.
echo ========================================
echo   PIP环境问题
echo ========================================
echo.
echo 解决方案:
echo 1. 重新安装Python
echo 2. 或运行: python -m ensurepip --upgrade
echo 3. 或运行: python get-pip.py
echo.
pause
goto end

:file_error
echo.
echo ========================================
echo   文件缺失问题
echo ========================================
echo.
echo 解决方案:
echo 1. 确保在正确的目录运行脚本
echo 2. 检查文件是否被删除或移动
echo 3. 重新下载项目文件
echo.
pause

:end
endlocal