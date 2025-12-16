#!/bin/bash
# iGreen+ Backend Systemd 服务卸载脚本

set -e

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

SERVICE_NAME="igreen-backend"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "========================================="
echo "iGreen+ Backend Service 卸载程序"
echo "========================================="

# 确认卸载
read -p "确认卸载 systemd 服务? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 1
fi

# 停止服务
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "停止服务..."
    systemctl stop $SERVICE_NAME
fi

# 禁用服务
if systemctl is-enabled --quiet $SERVICE_NAME; then
    echo "禁用服务..."
    systemctl disable $SERVICE_NAME
fi

# 删除服务文件
if [ -f "$SERVICE_FILE" ]; then
    echo "删除服务文件..."
    rm -f "$SERVICE_FILE"
fi

# 重新加载systemd
echo "重新加载 systemd 配置..."
systemctl daemon-reload
systemctl reset-failed

echo ""
echo "========================================="
echo "✓ 卸载完成!"
echo "========================================="
echo ""
echo "注意: 以下内容未删除，如需删除请手动处理:"
echo "  - 后端代码目录"
echo "  - 日志文件 (/var/log/igreen/)"
echo "  - 虚拟环境 (venv/)"
echo ""
