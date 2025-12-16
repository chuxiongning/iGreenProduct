#!/bin/bash
# iGreen+ Backend 启动脚本
# 使用虚拟环境启动后端服务

set -e

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}iGreen+ Backend Startup Script${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}虚拟环境不存在，正在创建...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
fi

# 激活虚拟环境
echo -e "${YELLOW}激活虚拟环境...${NC}"
source venv/bin/activate

# 检查依赖是否已安装
if [ ! -f "venv/.dependencies_installed" ]; then
    echo -e "${YELLOW}安装Python依赖...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.dependencies_installed
    echo -e "${GREEN}✓ 依赖安装完成${NC}"
else
    echo -e "${GREEN}✓ 依赖已安装${NC}"
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo -e "${RED}⚠️  警告: .env 文件不存在${NC}"
    echo -e "${YELLOW}正在从 .env.example 创建 .env 文件...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}请编辑 .env 文件配置数据库连接信息${NC}"
    echo -e "${RED}按 Ctrl+C 取消，或按 Enter 继续使用默认配置（SQLite）${NC}"
    read
fi

# 检查数据库是否初始化
if [ ! -f "igreen.db" ] && [ ! -f ".db_initialized" ]; then
    echo -e "${YELLOW}数据库未初始化，是否现在初始化? (y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        python scripts/init_db.py
        touch .db_initialized
        echo -e "${GREEN}✓ 数据库初始化完成${NC}"
    fi
fi

# 创建uploads目录
mkdir -p uploads

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}启动服务器...${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}API文档: http://localhost:8000/docs${NC}"
echo -e "${YELLOW}健康检查: http://localhost:8000/api/health${NC}"
echo -e "${GREEN}========================================${NC}"

# 启动服务器
# 开发环境使用 uvicorn 的热重载
if [ "${ENVIRONMENT:-development}" = "production" ]; then
    # 生产环境使用 gunicorn
    exec gunicorn main:app \
        --workers 4 \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind 0.0.0.0:8000 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile -
else
    # 开发环境
    exec uvicorn main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload
fi
