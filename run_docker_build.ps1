# rPPG生理指标检测系统 - Docker构建脚本 (PowerShell版本)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  rPPG生理指标检测系统 - Docker构建" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 切换到项目目录
$projectDir = "D:\rPPG安卓化"
Set-Location $projectDir

# 步骤1: 准备构建环境
Write-Host "[1/3] 准备构建环境..." -ForegroundColor Yellow
if (Test-Path "main.py") {
    Copy-Item "main.py" "main_original.py" -Force
}
if (Test-Path "main_webview.py") {
    Copy-Item "main_webview.py" "main.py" -Force
    Write-Host "已切换到WebView版本" -ForegroundColor Green
}
Write-Host ""

# 步骤2: 创建Dockerfile
Write-Host "[2/3] 创建Dockerfile(使用阿里云镜像)..." -ForegroundColor Yellow
$dockerfileContent = @"
FROM registry.cn-hangzhou.aliyuncs.com/library/ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
ENV ANDROIDSDK=/root/.buildozer/android/platform/android-sdk
ENV ANDROIDNDK=/root/.buildozer/android/platform/android-ndk-r25b
ENV ANDROIDAPI=33
ENV ANDROIDMINAPI=21

RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y python3 python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libffi-dev libssl-dev automake cmake && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && pip3 install buildozer cython kivy -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

COPY . /app/

CMD ["buildozer", "-v", "android", "debug"]
"@

$dockerfileContent | Out-File -FilePath "Dockerfile" -Encoding UTF8
Write-Host "Dockerfile创建完成" -ForegroundColor Green
Write-Host ""

# 步骤3: 构建Docker镜像
Write-Host "[3/3] 开始构建APK..." -ForegroundColor Yellow
Write-Host "注意: 首次构建需要30-60分钟，请耐心等待" -ForegroundColor Red
Write-Host ""

# 尝试找到docker命令
$dockerPath = $null
$possiblePaths = @(
    "C:\Program Files\Docker\Docker\resources\bin\docker.exe",
    "C:\ProgramData\DockerDesktop\version-bin\docker.exe",
    "${env:ProgramFiles}\Docker\Docker\resources\bin\docker.exe",
    "${env:LOCALAPPDATA}\Programs\Docker\Docker\resources\bin\docker.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $dockerPath = $path
        break
    }
}

if (-not $dockerPath) {
    # 尝试从环境变量找
    $dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
    if ($dockerCmd) {
        $dockerPath = $dockerCmd.Source
    }
}

if ($dockerPath) {
    Write-Host "找到Docker: $dockerPath" -ForegroundColor Green
    Write-Host "开始构建Docker镜像..." -ForegroundColor Yellow
    
    # 构建镜像
    & $dockerPath build -t rppg-builder .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Docker镜像构建成功，开始构建APK..." -ForegroundColor Green
        & $dockerPath run --rm -v "${projectDir}:/app" rppg-builder
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "  构建成功！" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Green
            Write-Host ""
            
            if (Test-Path "bin\*.apk") {
                Write-Host "APK文件:" -ForegroundColor Yellow
                Get-ChildItem "bin\*.apk" | ForEach-Object { Write-Host $_.Name }
            }
        } else {
            Write-Host ""
            Write-Host "APK构建失败" -ForegroundColor Red
        }
    } else {
        Write-Host ""
        Write-Host "Docker镜像构建失败" -ForegroundColor Red
        Write-Host ""
        Write-Host "可能的解决方案:" -ForegroundColor Yellow
        Write-Host "1. 检查网络连接" -ForegroundColor White
        Write-Host "2. 配置Docker使用代理" -ForegroundColor White
        Write-Host "3. 尝试使用WSL方案: wsl --install -d Ubuntu" -ForegroundColor White
        Write-Host "4. 使用GitHub Actions在线构建" -ForegroundColor White
    }
} else {
    Write-Host "错误: 未找到Docker命令" -ForegroundColor Red
    Write-Host "请确保Docker Desktop已正确安装并运行" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "你可以尝试:" -ForegroundColor Yellow
    Write-Host "1. 重启Docker Desktop" -ForegroundColor White
    Write-Host "2. 重启电脑后重试" -ForegroundColor White
    Write-Host "3. 使用WSL方案" -ForegroundColor White
}

# 恢复原始main.py
if (Test-Path "main_original.py") {
    Copy-Item "main_original.py" "main.py" -Force
    Remove-Item "main_original.py" -Force
}

Write-Host ""
Read-Host "按Enter键继续"
