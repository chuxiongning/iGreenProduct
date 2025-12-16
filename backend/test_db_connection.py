#!/usr/bin/env python3
"""
数据库连接测试脚本
用于验证数据库配置是否正确
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from sqlalchemy import create_engine, text

def test_connection():
    """测试数据库连接"""
    print("=" * 50)
    print("iGreen+ 数据库连接测试")
    print("=" * 50)
    print()
    
    # 显示配置信息（隐藏密码）
    print(f"数据库类型: {settings.DATABASE_TYPE}")
    
    if settings.DATABASE_TYPE == "mysql":
        print(f"数据库主机: {settings.DATABASE_HOST}")
        print(f"数据库端口: {settings.DATABASE_PORT}")
        print(f"数据库名称: {settings.DATABASE_NAME}")
        print(f"数据库用户: {settings.DATABASE_USER}")
        print(f"数据库密码: {'*' * len(settings.DATABASE_PASSWORD) if settings.DATABASE_PASSWORD else '(未设置)'}")
    
    print()
    print(f"连接字符串: {settings.DATABASE_URL.split('://')[0]}://...")
    print()
    print("正在测试连接...")
    print()
    
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)
        
        # 尝试连接
        with engine.connect() as conn:
            # 执行简单查询
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
            if row[0] == 1:
                print("✓ 数据库连接成功！")
                print()
                
                # 获取数据库版本
                try:
                    if settings.DATABASE_TYPE == "mysql":
                        version_result = conn.execute(text("SELECT VERSION()"))
                        version = version_result.fetchone()[0]
                        print(f"MySQL 版本: {version}")
                    else:
                        print("SQLite 数据库")
                except:
                    pass
                
                print()
                print("=" * 50)
                print("测试通过！可以运行 python scripts/init_db.py")
                print("=" * 50)
                return True
                
    except Exception as e:
        print("✗ 数据库连接失败！")
        print()
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print()
        print("=" * 50)
        print("故障排除建议:")
        print("=" * 50)
        
        if "Access denied" in str(e):
            print("❌ 权限错误 - 用户名或密码不正确")
            print()
            print("解决方案:")
            print("1. 运行自动设置脚本:")
            print("   ./setup_mysql.sh")
            print()
            print("2. 或手动创建数据库:")
            print("   mysql -u root -p")
            print("   CREATE DATABASE igreen_db;")
            print("   CREATE USER 'igreen_user'@'localhost' IDENTIFIED BY 'password';")
            print("   GRANT ALL ON igreen_db.* TO 'igreen_user'@'localhost';")
            print()
            print("3. 或使用 SQLite 进行测试:")
            print("   编辑 .env 文件，设置 DATABASE_TYPE=sqlite")
            
        elif "Can't connect" in str(e) or "Connection refused" in str(e):
            print("❌ 无法连接 - MySQL 服务可能未运行")
            print()
            print("检查 MySQL 服务:")
            print("   sudo systemctl status mysql")
            print()
            print("启动 MySQL:")
            print("   sudo systemctl start mysql")
            
        elif "Unknown database" in str(e):
            print("❌ 数据库不存在")
            print()
            print("创建数据库:")
            print("   mysql -u root -p")
            print("   CREATE DATABASE igreen_db;")
            print()
            print("或运行自动设置脚本:")
            print("   ./setup_mysql.sh")
            
        else:
            print("检查以下内容:")
            print("1. MySQL 服务是否运行")
            print("2. .env 文件配置是否正确")
            print("3. 数据库和用户是否已创建")
            print()
            print("查看完整故障排除指南:")
            print("   cat TROUBLESHOOTING_DB.md")
        
        print()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
