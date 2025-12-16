# iGreen+ Backend 服务管理指南

本文档说明如何使用Python虚拟环境运行后端，以及如何将后端设置为systemd系统服务。

## 目录
- [开发环境使用](#开发环境使用)
- [生产环境 - Systemd 服务](#生产环境---systemd-服务)
- [常用命令](#常用命令)
- [故障排除](#故障排除)

---

## 开发环境使用

### 快速启动

使用提供的启动脚本（自动管理虚拟环境）：

```bash
cd backend
./start.sh
```

启动脚本会自动：
1. 创建虚拟环境（如果不存在）
2. 安装所有依赖
3. 检查 `.env` 配置
4. 提示初始化数据库（如需要）
5. 启动开发服务器（带热重载）

### 手动启动（分步骤）

如果您想手动控制每一步：

```bash
cd backend

# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
nano .env  # 编辑配置

# 5. 初始化数据库
python scripts/init_db.py

# 6. 启动服务器
# 开发模式（带热重载）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 或生产模式
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 停止服务

```bash
# 使用停止脚本
./stop.sh

# 或手动停止
# Ctrl+C 停止前台运行的服务
```

---

## 生产环境 - Systemd 服务

### 一键安装服务

使用提供的安装脚本：

```bash
cd backend
sudo ./install_service.sh
```

安装脚本会：
1. 创建虚拟环境
2. 安装所有依赖（包括 gunicorn）
3. 创建 systemd 服务文件
4. 配置日志目录
5. 启用开机自启
6. 询问是否立即启动服务

### 手动安装服务

如果需要手动安装：

#### 1. 准备虚拟环境

```bash
cd /opt/iGreenProduct/backend  # 或您的部署目录

# 创建虚拟环境
python3 -m venv venv

# 激活并安装依赖
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # 生产环境需要
```

#### 2. 创建 systemd 服务文件

```bash
sudo nano /etc/systemd/system/igreen-backend.service
```

粘贴以下内容（**注意修改路径和用户名**）：

```ini
[Unit]
Description=iGreen+ Backend API Service
Documentation=https://github.com/chuxiongning/iGreenProduct
After=network.target mysql.service
Wants=mysql.service

[Service]
Type=notify
User=YOUR_USERNAME
Group=YOUR_USERNAME
WorkingDirectory=/opt/iGreenProduct/backend

# 环境变量 - 使用虚拟环境的路径
Environment="PATH=/opt/iGreenProduct/backend/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="ENVIRONMENT=production"

# 启动命令 - 使用虚拟环境中的gunicorn
ExecStart=/opt/iGreenProduct/backend/venv/bin/gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile /var/log/igreen/access.log \
    --error-logfile /var/log/igreen/error.log \
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
```

**重要配置说明：**

- `User` 和 `Group`: 改为实际运行用户（通常是部署用户，不要用 root）
- `WorkingDirectory`: 后端代码的实际路径
- `Environment="PATH=..."`: 必须包含虚拟环境的 bin 目录
- `ExecStart`: 使用虚拟环境中的 gunicorn（绝对路径）

#### 3. 创建日志目录

```bash
sudo mkdir -p /var/log/igreen
sudo chown YOUR_USERNAME:YOUR_USERNAME /var/log/igreen
```

#### 4. 配置文件权限

```bash
sudo chown -R YOUR_USERNAME:YOUR_USERNAME /opt/iGreenProduct/backend
```

#### 5. 启用并启动服务

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启用开机自启
sudo systemctl enable igreen-backend

# 启动服务
sudo systemctl start igreen-backend

# 检查状态
sudo systemctl status igreen-backend
```

---

## 常用命令

### 服务管理

```bash
# 启动服务
sudo systemctl start igreen-backend

# 停止服务
sudo systemctl stop igreen-backend

# 重启服务
sudo systemctl restart igreen-backend

# 重新加载配置（不中断服务）
sudo systemctl reload igreen-backend

# 查看服务状态
sudo systemctl status igreen-backend

# 启用开机自启
sudo systemctl enable igreen-backend

# 禁用开机自启
sudo systemctl disable igreen-backend
```

### 日志查看

```bash
# 查看实时日志
sudo journalctl -u igreen-backend -f

# 查看最近100行日志
sudo journalctl -u igreen-backend -n 100

# 查看今天的日志
sudo journalctl -u igreen-backend --since today

# 查看错误日志
sudo journalctl -u igreen-backend -p err

# 查看应用日志文件
sudo tail -f /var/log/igreen/access.log
sudo tail -f /var/log/igreen/error.log
```

### 虚拟环境管理

```bash
# 激活虚拟环境
cd backend
source venv/bin/activate

# 更新依赖
pip install -r requirements.txt --upgrade

# 查看已安装的包
pip list

# 退出虚拟环境
deactivate
```

### 更新代码后重启

```bash
# 拉取最新代码
cd /opt/iGreenProduct
git pull

# 更新依赖（如果 requirements.txt 有变化）
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 重启服务
sudo systemctl restart igreen-backend

# 查看启动状态
sudo systemctl status igreen-backend
```

---

## 故障排除

### 1. 服务启动失败

**查看详细错误**：
```bash
sudo journalctl -u igreen-backend -n 50 --no-pager
```

**常见原因**：
- 虚拟环境路径错误
- Python 依赖未安装
- 数据库连接失败
- 端口被占用

### 2. 虚拟环境问题

**重新创建虚拟环境**：
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 3. 权限问题

**修复文件权限**：
```bash
sudo chown -R YOUR_USERNAME:YOUR_USERNAME /opt/iGreenProduct/backend
sudo chown -R YOUR_USERNAME:YOUR_USERNAME /var/log/igreen
```

### 4. 端口被占用

**检查端口占用**：
```bash
sudo netstat -tulpn | grep 8000
# 或
sudo lsof -i :8000
```

**停止占用端口的进程**：
```bash
sudo kill -9 PID  # 替换 PID 为实际进程ID
```

### 5. 数据库连接问题

**检查 MySQL 服务**：
```bash
sudo systemctl status mysql
```

**测试数据库连接**：
```bash
mysql -u igreen_user -p igreen_db
```

**检查 .env 配置**：
```bash
cat backend/.env | grep DATABASE
```

### 6. 查看Python错误

**激活虚拟环境并手动运行**：
```bash
cd backend
source venv/bin/activate
python main.py
```

这样可以看到详细的Python错误信息。

---

## 卸载服务

使用卸载脚本：

```bash
cd backend
sudo ./uninstall_service.sh
```

或手动卸载：

```bash
# 停止并禁用服务
sudo systemctl stop igreen-backend
sudo systemctl disable igreen-backend

# 删除服务文件
sudo rm /etc/systemd/system/igreen-backend.service

# 重新加载 systemd
sudo systemctl daemon-reload
```

---

## 性能优化

### 调整 Worker 数量

编辑服务文件中的 `--workers` 参数：

```bash
sudo nano /etc/systemd/system/igreen-backend.service
```

**推荐配置**：
- CPU密集型: `workers = (CPU核心数 × 2) + 1`
- I/O密集型: `workers = CPU核心数 × 2`

示例：
```ini
# 4核CPU建议配置
ExecStart=.../gunicorn main:app --workers 8 ...
```

修改后重启：
```bash
sudo systemctl daemon-reload
sudo systemctl restart igreen-backend
```

### 监控资源使用

```bash
# 查看服务资源使用
systemctl status igreen-backend

# 详细资源信息
systemd-cgtop
```

---

## 自动化维护

### 设置日志轮转

创建 `/etc/logrotate.d/igreen-backend`：

```bash
sudo nano /etc/logrotate.d/igreen-backend
```

```
/var/log/igreen/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 YOUR_USERNAME YOUR_USERNAME
    sharedscripts
    postrotate
        systemctl reload igreen-backend > /dev/null 2>&1 || true
    endscript
}
```

### 设置自动备份

参考主文档中的备份脚本，配置定时任务。

---

## 总结

- **开发环境**: 使用 `./start.sh` 快速启动
- **生产环境**: 使用 `sudo ./install_service.sh` 安装为系统服务
- **虚拟环境**: 确保所有路径正确指向 `venv/bin/`
- **日志**: 使用 `journalctl` 和应用日志文件排查问题

如有问题，请检查日志或参考故障排除部分。
