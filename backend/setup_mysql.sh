#!/bin/bash
# MySQL 数据库设置脚本
# 自动创建数据库和用户

set -e

echo "========================================="
echo "iGreen+ MySQL 数据库设置向导"
echo "========================================="
echo ""

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 默认配置
DB_NAME="igreen_db"
DB_USER="igreen_user"
DB_PASSWORD=""

# 读取.env文件中的配置（如果存在）
if [ -f ".env" ]; then
    echo -e "${YELLOW}检测到 .env 文件，读取配置...${NC}"
    source .env
    DB_NAME=${DATABASE_NAME:-igreen_db}
    DB_USER=${DATABASE_USER:-igreen_user}
    DB_PASSWORD=${DATABASE_PASSWORD}
fi

# 如果密码为空，提示输入
if [ -z "$DB_PASSWORD" ]; then
    echo -e "${YELLOW}请设置数据库密码${NC}"
    read -sp "输入 MySQL 数据库密码 (为 $DB_USER 用户): " DB_PASSWORD
    echo ""
fi

echo ""
echo "将使用以下配置:"
echo "  数据库名: $DB_NAME"
echo "  用户名:   $DB_USER"
echo "  密码:     ********"
echo ""

# 询问 MySQL root 密码
echo -e "${YELLOW}请输入 MySQL root 用户密码以创建数据库:${NC}"
read -sp "MySQL root 密码: " MYSQL_ROOT_PASSWORD
echo ""

echo ""
echo "开始设置数据库..."
echo ""

# 创建SQL命令
SQL_COMMANDS="
-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 删除旧用户（如果存在）
DROP USER IF EXISTS '${DB_USER}'@'localhost';
DROP USER IF EXISTS '${DB_USER}'@'%';

-- 创建新用户
CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
CREATE USER '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';

-- 授予权限
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 显示用户权限
SHOW GRANTS FOR '${DB_USER}'@'localhost';
"

# 执行SQL命令
if mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "${SQL_COMMANDS}" 2>/dev/null; then
    echo ""
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}✓ 数据库设置成功！${NC}"
    echo -e "${GREEN}=========================================${NC}"
    echo ""
    echo "数据库信息:"
    echo "  数据库名: $DB_NAME"
    echo "  用户名:   $DB_USER"
    echo "  主机:     localhost (或远程IP)"
    echo ""

    # 更新 .env 文件
    if [ -f ".env" ]; then
        echo -e "${YELLOW}更新 .env 文件...${NC}"

        # 备份原文件
        cp .env .env.backup

        # 更新配置
        sed -i "s/^DATABASE_TYPE=.*/DATABASE_TYPE=mysql/" .env
        sed -i "s/^DATABASE_NAME=.*/DATABASE_NAME=$DB_NAME/" .env
        sed -i "s/^DATABASE_USER=.*/DATABASE_USER=$DB_USER/" .env
        sed -i "s/^DATABASE_PASSWORD=.*/DATABASE_PASSWORD=$DB_PASSWORD/" .env

        echo -e "${GREEN}✓ .env 文件已更新${NC}"
    else
        echo -e "${YELLOW}创建 .env 文件...${NC}"
        cp .env.example .env
        sed -i "s/^DATABASE_TYPE=.*/DATABASE_TYPE=mysql/" .env
        sed -i "s/^DATABASE_NAME=.*/DATABASE_NAME=$DB_NAME/" .env
        sed -i "s/^DATABASE_USER=.*/DATABASE_USER=$DB_USER/" .env
        sed -i "s/^DATABASE_PASSWORD=.*/DATABASE_PASSWORD=$DB_PASSWORD/" .env
        echo -e "${GREEN}✓ .env 文件已创建${NC}"
    fi

    echo ""
    echo -e "${GREEN}现在可以运行以下命令初始化数据库:${NC}"
    echo "  python scripts/init_db.py"
    echo ""

else
    echo ""
    echo -e "${RED}❌ 数据库设置失败${NC}"
    echo ""
    echo "可能的原因:"
    echo "  1. MySQL root 密码不正确"
    echo "  2. MySQL 服务未运行"
    echo "  3. 权限不足"
    echo ""
    echo "请检查 MySQL 服务状态:"
    echo "  sudo systemctl status mysql"
    echo ""
    exit 1
fi
