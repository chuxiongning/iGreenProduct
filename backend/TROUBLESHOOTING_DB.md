# 数据库设置故障排除指南

当运行 `python scripts/init_db.py` 时遇到权限错误，请按照以下步骤解决。

## 错误信息
```
Access denied for user 'igreen_user'@'%' to database 'igreen_db'
```

## 解决方案

### 方案1：使用 SQLite（推荐用于快速测试）

最简单的方法是先使用 SQLite 测试系统：

```bash
cd backend

# 1. 编辑 .env 文件
nano .env

# 2. 修改以下配置
DATABASE_TYPE=sqlite
# 注释掉其他 MySQL 配置

# 3. 初始化数据库
python scripts/init_db.py

# 4. 启动服务
./start.sh
```

这样会创建一个本地的 `igreen.db` SQLite 数据库文件，无需配置 MySQL。

---

### 方案2：自动设置 MySQL（推荐）

使用我们提供的自动化脚本：

```bash
cd backend

# 运行 MySQL 设置脚本
./setup_mysql.sh
```

脚本会：
1. 询问数据库密码
2. 询问 MySQL root 密码
3. 自动创建数据库
4. 创建用户并授予权限
5. 更新 .env 文件

然后运行：
```bash
python scripts/init_db.py
```

---

### 方案3：手动设置 MySQL

#### 步骤1：登录 MySQL

```bash
mysql -u root -p
```

输入 MySQL root 密码。

#### 步骤2：创建数据库和用户

```sql
-- 创建数据库
CREATE DATABASE igreen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（localhost连接）
CREATE USER 'igreen_user'@'localhost' IDENTIFIED BY 'your_password_here';

-- 创建用户（远程连接）
CREATE USER 'igreen_user'@'%' IDENTIFIED BY 'your_password_here';

-- 授予权限
GRANT ALL PRIVILEGES ON igreen_db.* TO 'igreen_user'@'localhost';
GRANT ALL PRIVILEGES ON igreen_db.* TO 'igreen_user'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 验证权限
SHOW GRANTS FOR 'igreen_user'@'localhost';

-- 退出
EXIT;
```

**重要**: 将 `your_password_here` 替换为您的实际密码！

#### 步骤3：更新 .env 文件

```bash
cd backend
nano .env
```

确保以下配置正确：

```env
DATABASE_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=igreen_user
DATABASE_PASSWORD=your_password_here
DATABASE_NAME=igreen_db
```

#### 步骤4：测试连接

```bash
# 测试 MySQL 连接
mysql -u igreen_user -p igreen_db

# 如果能成功登录，说明权限配置正确
# 输入密码后应该能看到 MySQL 提示符
# 输入 EXIT; 退出
```

#### 步骤5：初始化数据库

```bash
python scripts/init_db.py
```

---

## 常见问题

### Q1: MySQL 服务未运行

**检查服务状态：**
```bash
sudo systemctl status mysql
```

**启动 MySQL：**
```bash
sudo systemctl start mysql
```

**设置开机自启：**
```bash
sudo systemctl enable mysql
```

### Q2: 忘记 MySQL root 密码

**Ubuntu/Debian 系统：**
```bash
sudo mysql

# 然后执行：
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new_password';
FLUSH PRIVILEGES;
EXIT;
```

**CentOS/RHEL 系统：**
```bash
sudo systemctl stop mysql
sudo mysqld_safe --skip-grant-tables &
mysql -u root

# 执行密码重置
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
EXIT;

sudo systemctl restart mysql
```

### Q3: 权限被拒绝（即使已授权）

**刷新权限：**
```bash
mysql -u root -p
FLUSH PRIVILEGES;
EXIT;
```

**重启 MySQL：**
```bash
sudo systemctl restart mysql
```

### Q4: 无法连接到远程 MySQL

如果 MySQL 在另一台服务器上：

**1. 检查防火墙：**
```bash
sudo ufw allow 3306/tcp
```

**2. 修改 MySQL 配置允许远程连接：**
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

找到并修改：
```ini
bind-address = 0.0.0.0
```

重启 MySQL：
```bash
sudo systemctl restart mysql
```

**3. 确保用户有远程访问权限：**
```sql
GRANT ALL PRIVILEGES ON igreen_db.* TO 'igreen_user'@'%';
FLUSH PRIVILEGES;
```

### Q5: 字符集问题

确保数据库使用 UTF8MB4：

```sql
ALTER DATABASE igreen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 验证配置

创建测试脚本 `test_db.py`：

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from app.core.config import settings
from sqlalchemy import create_engine, text

print(f"Testing connection to: {settings.DATABASE_URL}")

try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✓ Database connection successful!")
        print(f"✓ Database: {settings.DATABASE_NAME}")
        print(f"✓ User: {settings.DATABASE_USER}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    sys.exit(1)
```

运行测试：
```bash
python test_db.py
```

---

## 快速参考

### SQLite（开发/测试）
```env
DATABASE_TYPE=sqlite
```

### MySQL（生产环境）
```env
DATABASE_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=igreen_user
DATABASE_PASSWORD=your_secure_password
DATABASE_NAME=igreen_db
```

---

## 推荐的设置流程

**开发环境：**
1. 使用 SQLite（无需配置）
2. 测试所有功能
3. 稍后迁移到 MySQL

**生产环境：**
1. 运行 `./setup_mysql.sh` 自动设置
2. 或手动创建数据库和用户
3. 运行 `python scripts/init_db.py`
4. 使用 `./start.sh` 或安装为服务

---

如果以上方案都无法解决问题，请提供：
1. MySQL 版本：`mysql --version`
2. 错误日志：`sudo tail -f /var/log/mysql/error.log`
3. 用户权限：`SHOW GRANTS FOR 'igreen_user'@'localhost';`
