#!/bin/bash
# iGreen+ Backend Systemd 服务安装脚本

set -e

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 获取当前用户（实际运行sudo的用户）
ACTUAL_USER=${SUDO_USER:-$USER}
ACTUAL_HOME=$(eval echo ~$ACTUAL_USER)

# 获取脚本所在目录的绝对路径
BACKEND_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "========================================="
echo "iGreen+ Backend Service 安装程序"
echo "========================================="
echo "后端目录: $BACKEND_DIR"
echo "运行用户: $ACTUAL_USER"
echo "========================================="

# 确认安装
read -p "确认安装 systemd 服务? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "安装已取消"
    exit 1
fi

# 创建systemd服务文件
SERVICE_FILE="/etc/systemd/system/igreen-backend.service"

echo "创建 systemd 服务文件: $SERVICE_FILE"

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=iGreen+ Backend API Service
Documentation=https://github.com/chuxiongning/iGreenProduct
After=network.target mysql.service
Wants=mysql.service

[Service]
Type=notify
User=$ACTUAL_USER
Group=$ACTUAL_USER
WorkingDirectory=$BACKEND_DIR

# 环境变量
Environment="PATH=$BACKEND_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="ENVIRONMENT=production"

# 启动命令 - 使用虚拟环境中的gunicorn
ExecStart=$BACKEND_DIR/venv/bin/gunicorn main:app \\
    --workers 4 \\
    --worker-class uvicorn.workers.UvicornWorker \\
    --bind 0.0.0.0:8000 \\
    --timeout 120 \\
    --access-logfile /var/log/igreen/access.log \\
    --error-logfile /var/log/igreen/error.log \\
    --log-level info

# 重启策略
Restart=always
RestartSec=10
StartLimitInterval=5min
StartLimitBurst=5

# 资源限制
LimitNOFILE=65536

# 安全设置
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# 创建日志目录
echo "创建日志目录..."
mkdir -p /var/log/igreen
chown $ACTUAL_USER:$ACTUAL_USER /var/log/igreen

# 确保虚拟环境存在
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "创建Python虚拟环境..."
    su - $ACTUAL_USER -c "cd $BACKEND_DIR && python3 -m venv venv"
fi

# 安装依赖
echo "安装Python依赖..."
su - $ACTUAL_USER -c "cd $BACKEND_DIR && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn"

# 设置文件权限
echo "设置文件权限..."
chown -R $ACTUAL_USER:$ACTUAL_USER "$BACKEND_DIR"
chmod 755 "$BACKEND_DIR"

# 重新加载systemd
echo "重新加载 systemd 配置..."
systemctl daemon-reload

# 启用服务
echo "启用服务开机自启..."
systemctl enable igreen-backend.service

echo ""
echo "========================================="
echo "✓ 安装完成!"
echo "========================================="
echo ""
echo "使用以下命令管理服务:"
echo "  启动服务:   sudo systemctl start igreen-backend"
echo "  停止服务:   sudo systemctl stop igreen-backend"
echo "  重启服务:   sudo systemctl restart igreen-backend"
echo "  查看状态:   sudo systemctl status igreen-backend"
echo "  查看日志:   sudo journalctl -u igreen-backend -f"
echo ""
echo "日志文件位置:"
echo "  访问日志:   /var/log/igreen/access.log"
echo "  错误日志:   /var/log/igreen/error.log"
echo ""

# 询问是否立即启动
read -p "是否现在启动服务? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl start igreen-backend
    sleep 2
    systemctl status igreen-backend
fi
