@echo off
chcp 65001 >nul
echo ====================================
echo   MonitorTask 漏洞情报监控平台
echo ====================================
echo.

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未配置到PATH
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python环境正常

echo.
echo [2/4] 检查虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo ✅ 虚拟环境创建成功
) else (
    echo ✅ 虚拟环境已存在
)

echo.
echo [3/4] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成

echo.
echo [4/4] 检查配置文件...
if not exist ".env" (
    echo 复制配置文件...
    copy .env.example .env
    echo ⚠️  请编辑 .env 文件配置相关参数
)

echo.
echo ====================================
echo   启动MonitorTask服务
echo ====================================
echo.
echo 🚀 服务启动中...
echo 📡 后端API: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务
echo ====================================
echo.

python run.py

pause
