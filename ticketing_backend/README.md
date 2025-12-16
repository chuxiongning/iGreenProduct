# iGreen Ticketing System - Backend API

FastAPI后端服务，用于iGreen EV充电站维护工单系统。

## 技术栈

- **框架**: FastAPI 0.109.0
- **数据库**: MySQL (使用SQLAlchemy ORM)
- **认证**: JWT (使用python-jose)
- **密码加密**: bcrypt (使用passlib)
- **数据验证**: Pydantic
- **服务器**: Uvicorn

## 项目结构

```
backend/
├── app/
│   ├── api/              # API路由
│   │   ├── auth.py       # 认证接口
│   │   ├── users.py      # 用户管理
│   │   ├── tickets.py    # 工单管理
│   │   ├── templates.py  # 模板管理
│   │   ├── groups.py     # 分组管理
│   │   ├── sites.py      # 站点管理
│   │   ├── configs.py    # 系统配置
│   │   └── files.py      # 文件上传
│   ├── models/           # SQLAlchemy数据库模型
│   ├── schemas/          # Pydantic数据模型
│   ├── utils/            # 工具函数
│   ├── config.py         # 配置文件
│   └── database.py       # 数据库连接
├── main.py               # 应用入口
├── requirements.txt      # Python依赖
├── .env.example          # 环境变量示例
└── README.md             # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置MySQL数据库连接：

```env
# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=igreen_user
DATABASE_PASSWORD=your_password
DATABASE_NAME=igreen_ticketing

# JWT密钥 (请使用安全的随机字符串)
SECRET_KEY=your-secret-key-here

# 其他配置...
```

### 3. 创建数据库

登录MySQL并创建数据库：

```sql
CREATE DATABASE igreen_ticketing CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'igreen_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON igreen_ticketing.* TO 'igreen_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. 运行应用

开发模式（自动重载）：

```bash
python main.py
```

或使用uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问API文档

应用启动后，访问以下地址查看API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API信息**: http://localhost:8000/

## API端点

### 认证 (Authentication)

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/logout` - 用户登出

### 用户管理 (Users)

- `GET /api/users` - 获取所有用户
- `GET /api/users/{id}` - 获取指定用户
- `POST /api/users` - 创建用户
- `PUT /api/users/{id}` - 更新用户
- `DELETE /api/users/{id}` - 删除用户

### 工单管理 (Tickets)

- `GET /api/tickets` - 获取所有工单
- `GET /api/tickets/{id}` - 获取指定工单
- `POST /api/tickets` - 创建工单
- `PUT /api/tickets/{id}` - 更新工单
- `DELETE /api/tickets/{id}` - 删除工单
- `POST /api/tickets/{id}/accept` - 接受工单
- `POST /api/tickets/{id}/decline` - 拒绝工单
- `POST /api/tickets/{id}/cancel` - 取消工单

### 模板管理 (Templates)

- `GET /api/templates` - 获取所有模板
- `GET /api/templates/{id}` - 获取指定模板
- `POST /api/templates` - 创建模板
- `PUT /api/templates/{id}` - 更新模板
- `DELETE /api/templates/{id}` - 删除模板

### 分组管理 (Groups)

- `GET /api/groups` - 获取所有分组
- `GET /api/groups/{id}` - 获取指定分组
- `POST /api/groups` - 创建分组
- `PUT /api/groups/{id}` - 更新分组
- `DELETE /api/groups/{id}` - 删除分组

### 站点管理 (Sites)

- `GET /api/sites` - 获取所有站点
- `GET /api/sites/{id}` - 获取指定站点
- `POST /api/sites` - 创建站点
- `PUT /api/sites/{id}` - 更新站点
- `DELETE /api/sites/{id}` - 删除站点

### 系统配置 (Configurations)

- `GET /api/sla-configs` - 获取SLA配置
- `POST /api/sla-configs` - 创建/更新SLA配置
- `GET /api/problem-types` - 获取问题类型
- `POST /api/problem-types` - 创建问题类型
- `GET /api/site-level-configs` - 获取站点级别配置
- `POST /api/site-level-configs` - 创建站点级别配置

### 文件上传 (Files)

- `POST /api/files/upload` - 上传文件
- `DELETE /api/files/{id}` - 删除文件
- `POST /api/files/face-recognition/verify` - 人脸识别验证

## 数据库迁移

建议使用Alembic进行数据库迁移：

### 初始化Alembic

```bash
alembic init alembic
```

### 创建迁移

```bash
alembic revision --autogenerate -m "Initial migration"
```

### 应用迁移

```bash
alembic upgrade head
```

## 开发指南

### 添加新的API端点

1. 在 `app/models/` 中定义数据库模型
2. 在 `app/schemas/` 中定义Pydantic模型
3. 在 `app/api/` 中创建路由文件
4. 在 `main.py` 中注册路由

### 代码规范

- 遵循PEP 8编码规范
- 使用类型提示
- 为函数添加文档字符串
- 使用有意义的变量名

### 测试

建议使用pytest进行测试：

```bash
pip install pytest pytest-asyncio httpx
pytest
```

## 部署

### 使用Docker

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：

```bash
docker build -t igreen-backend .
docker run -p 8000:8000 --env-file .env igreen-backend
```

### 生产环境

生产环境建议：

1. 使用环境变量管理配置
2. 启用HTTPS
3. 设置合适的CORS策略
4. 配置日志
5. 使用反向代理（Nginx）
6. 设置进程管理器（Supervisor, systemd等）

示例Nginx配置：

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 安全注意事项

- ✅ 修改默认的SECRET_KEY
- ✅ 使用强密码策略
- ✅ 定期更新依赖
- ✅ 启用HTTPS
- ✅ 限制CORS来源
- ✅ 实施速率限制
- ✅ 验证和清理用户输入
- ✅ 定期备份数据库

## 故障排除

### 数据库连接失败

检查：
- MySQL服务是否运行
- 数据库配置是否正确
- 用户权限是否正确

### 导入错误

确保所有依赖已安装：
```bash
pip install -r requirements.txt
```

## 许可证

MIT License

## 支持

如有问题，请联系开发团队或查看API文档。
