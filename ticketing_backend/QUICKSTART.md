# iGreen Ticketing System - 快速开始指南

本指南将帮助您在5分钟内启动并运行iGreen工单系统后端。

## 前提条件

- Python 3.9+
- MySQL 5.7+ 或 8.0+
- pip

## 步骤1: 安装MySQL并创建数据库

### 在Linux上安装MySQL:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server

# CentOS/RHEL
sudo yum install mysql-server
```

### 创建数据库:

```bash
# 登录MySQL
mysql -u root -p

# 在MySQL命令行中执行
CREATE DATABASE igreen_ticketing CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'igreen_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON igreen_ticketing.* TO 'igreen_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 步骤2: 克隆代码并安装依赖

```bash
cd iGreen_ticketingsys/backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 步骤3: 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件
nano .env  # 或使用你喜欢的编辑器
```

**重要**: 修改以下配置:

```env
# 数据库配置 - 必须修改
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=igreen_user
DATABASE_PASSWORD=your_secure_password  # 改为你的密码
DATABASE_NAME=igreen_ticketing

# JWT密钥 - 必须修改为安全的随机字符串
SECRET_KEY=your-very-secure-and-random-secret-key-here

# 允许的前端地址
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**生成安全的SECRET_KEY**:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 步骤4: 初始化数据库

```bash
# 运行数据库初始化脚本
python init_db.py
```

这将:
- 创建所有数据库表
- 创建默认用户账户
- 添加示例数据（SLA配置、问题类型等）

## 步骤5: 启动应用

```bash
# 开发模式启动（自动重载）
python main.py

# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

看到以下输出表示成功:

```
✅ iGreen Ticketing System started successfully!
📊 Database: localhost:3306/igreen_ticketing
🌐 CORS enabled for: http://localhost:3000, http://localhost:5173
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 步骤6: 测试API

打开浏览器访问:

- **API文档**: http://localhost:8000/docs
- **备用文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/api/health

### 测试登录

使用以下默认账户登录:

**管理员账户:**
```json
{
  "email": "admin@igreen.com",
  "password": "admin123"
}
```

**工程师账户:**
```json
{
  "email": "demo@csenergy.com",
  "password": "demo123"
}
```

**经理账户:**
```json
{
  "email": "manager@csenergy.com",
  "password": "manager123"
}
```

### 使用curl测试:

```bash
# 登录
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@igreen.com", "password": "admin123"}'

# 获取用户列表（需要token）
curl -X GET "http://localhost:8000/api/users" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 使用Swagger UI测试:

1. 访问 http://localhost:8000/docs
2. 点击 `/api/auth/login` 端点
3. 点击 "Try it out"
4. 输入登录凭证并执行
5. 复制返回的token
6. 点击页面顶部的 "Authorize" 按钮
7. 输入 `Bearer YOUR_TOKEN` 并授权
8. 现在可以测试其他需要认证的端点

## 常见问题

### 1. 数据库连接失败

**错误信息**: `Can't connect to MySQL server`

**解决方案**:
- 确认MySQL服务正在运行: `sudo systemctl status mysql`
- 检查.env中的数据库配置是否正确
- 确认数据库用户和密码正确
- 尝试手动连接: `mysql -u igreen_user -p igreen_ticketing`

### 2. 导入模块错误

**错误信息**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

### 3. 端口已被占用

**错误信息**: `[Errno 98] Address already in use`

**解决方案**:
```bash
# 查找占用8000端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
uvicorn main:app --port 8001
```

### 4. CORS错误

**错误信息**: 前端显示CORS policy错误

**解决方案**:
- 在.env中添加前端URL到`ALLOWED_ORIGINS`
- 重启后端服务

## 下一步

现在后端已经运行，你可以:

1. **启动前端**:
   ```bash
   cd ../  # 回到项目根目录
   npm run dev
   ```

2. **浏览API文档**: http://localhost:8000/docs

3. **创建新用户**: 使用`/api/auth/register`端点

4. **创建工单**: 使用`/api/tickets`端点

5. **自定义配置**: 修改SLA配置、添加站点等

## 生产部署

生产环境部署请参考 [README.md](README.md) 中的部署章节。

重要提示:
- ⚠️ 修改默认密码
- ⚠️ 使用强SECRET_KEY
- ⚠️ 启用HTTPS
- ⚠️ 配置防火墙
- ⚠️ 定期备份数据库

## 获取帮助

- 查看完整文档: [README.md](README.md)
- API规范: [API_SPECIFICATION.md](API_SPECIFICATION.md)
- 问题反馈: 联系开发团队

祝您使用愉快! 🎉
