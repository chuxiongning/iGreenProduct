#!/bin/bash
# iGreen+ Backend 停止脚本

echo "正在停止 iGreen+ Backend..."

# 查找并停止运行中的进程
pkill -f "uvicorn main:app" || true
pkill -f "gunicorn main:app" || true

echo "✓ 服务已停止"
