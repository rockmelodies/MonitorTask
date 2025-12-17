#!/bin/bash

echo "===================================="
echo "  MonitorTask 漏洞情报监控平台"
echo "===================================="
echo ""

echo "[1/4] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    echo "请先安装Python 3.8+"
    exit 1
fi
echo "✅ Python环境正常"

echo ""
echo "[2/4] 检查虚拟环境..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "✅ 虚拟环境已存在"
fi

echo ""
echo "[3/4] 激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✅ 依赖安装完成"

echo ""
echo "[4/4] 检查配置文件..."
if [ ! -f ".env" ]; then
    echo "复制配置文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件配置相关参数"
fi

echo ""
echo "===================================="
echo "  启动MonitorTask服务"
echo "===================================="
echo ""
echo "🚀 服务启动中..."
echo "📡 后端API: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务"
echo "===================================="
echo ""

python run.py
