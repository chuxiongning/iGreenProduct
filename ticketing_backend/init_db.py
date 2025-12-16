"""
数据库初始化脚本
创建初始数据（管理员用户、默认配置等）
"""
import uuid
from datetime import datetime, timedelta

from app.database import SessionLocal, init_db
from app.models.user import User, UserRole, UserStatus
from app.models.group import Group, GroupStatus
from app.models.site import Site, SiteStatus
from app.models.sla_config import SLAConfig
from app.models.ticket import Priority
from app.models.problem_type import ProblemType
from app.models.site_level_config import SiteLevelConfig
from app.models.template import Template, TemplateStep, TemplateField, FieldType
from app.utils.auth import get_password_hash


def create_initial_data():
    """创建初始数据"""
    db = SessionLocal()

    try:
        # 检查是否已有数据
        existing_user = db.query(User).first()
        if existing_user:
            print("⚠️  Database already contains data. Skipping initialization.")
            return

        print("🚀 Initializing database with sample data...")

        # 1. 创建管理员用户
        admin_user = User(
            id=str(uuid.uuid4()),
            name="System Administrator",
            username="admin",
            email="admin@igreen.com",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        db.add(admin_user)

        # 2. 创建演示用户
        demo_user = User(
            id=str(uuid.uuid4()),
            name="Demo Engineer",
            username="demo",
            email="demo@csenergy.com",
            hashed_password=get_password_hash("demo123"),
            role=UserRole.ENGINEER,
            status=UserStatus.ACTIVE
        )
        db.add(demo_user)

        manager_user = User(
            id=str(uuid.uuid4()),
            name="Demo Manager",
            username="manager",
            email="manager@csenergy.com",
            hashed_password=get_password_hash("manager123"),
            role=UserRole.MANAGER,
            status=UserStatus.ACTIVE
        )
        db.add(manager_user)

        # 3. 创建分组
        group1 = Group(
            id=str(uuid.uuid4()),
            name="Maintenance Team A",
            description="北部地区维护团队",
            tags=["north", "maintenance"],
            status=GroupStatus.ACTIVE
        )
        db.add(group1)

        group2 = Group(
            id=str(uuid.uuid4()),
            name="Maintenance Team B",
            description="南部地区维护团队",
            tags=["south", "maintenance"],
            status=GroupStatus.ACTIVE
        )
        db.add(group2)

        # 将演示工程师分配到组
        demo_user.group_id = group1.id

        # 4. 创建站点
        sites_data = [
            {"name": "Bangkok Central Station", "address": "Bangkok, Thailand", "level": "vip"},
            {"name": "Chiang Mai North", "address": "Chiang Mai, Thailand", "level": "normal"},
            {"name": "Phuket Beach Station", "address": "Phuket, Thailand", "level": "vip"},
            {"name": "Pattaya City Center", "address": "Pattaya, Thailand", "level": "normal"},
        ]

        for site_data in sites_data:
            site = Site(
                id=str(uuid.uuid4()),
                name=site_data["name"],
                address=site_data["address"],
                level=site_data["level"],
                status=SiteStatus.ONLINE
            )
            db.add(site)

        # 5. 创建SLA配置
        sla_configs = [
            {"priority": Priority.P1, "response_time": 30, "resolution_time": 240},    # P1: 30分钟响应, 4小时解决
            {"priority": Priority.P2, "response_time": 60, "resolution_time": 480},    # P2: 1小时响应, 8小时解决
            {"priority": Priority.P3, "response_time": 120, "resolution_time": 1440},  # P3: 2小时响应, 24小时解决
            {"priority": Priority.P4, "response_time": 240, "resolution_time": 2880},  # P4: 4小时响应, 48小时解决
        ]

        for config_data in sla_configs:
            sla_config = SLAConfig(
                id=str(uuid.uuid4()),
                priority=config_data["priority"],
                response_time=config_data["response_time"],
                resolution_time=config_data["resolution_time"]
            )
            db.add(sla_config)

        # 6. 创建问题类型
        problem_types = [
            {"name": "充电桩无法启动", "description": "充电桩设备无法正常启动"},
            {"name": "充电速度慢", "description": "充电速度明显低于正常水平"},
            {"name": "通信故障", "description": "设备与服务器通信异常"},
            {"name": "屏幕显示异常", "description": "显示屏无法正常显示或黑屏"},
            {"name": "支付系统故障", "description": "支付功能无法使用"},
        ]

        for pt_data in problem_types:
            problem_type = ProblemType(
                id=str(uuid.uuid4()),
                name=pt_data["name"],
                description=pt_data["description"]
            )
            db.add(problem_type)

        # 7. 创建站点级别配置
        site_levels = [
            {"name": "normal", "description": "普通站点", "sla_multiplier": 1.0},
            {"name": "vip", "description": "VIP站点 (SLA时间减半)", "sla_multiplier": 0.5},
        ]

        for level_data in site_levels:
            site_level_config = SiteLevelConfig(
                id=str(uuid.uuid4()),
                name=level_data["name"],
                description=level_data["description"],
                sla_multiplier=level_data["sla_multiplier"]
            )
            db.add(site_level_config)

        # 8. 创建示例模板
        template1 = Template(
            id=str(uuid.uuid4()),
            name="充电桩常规检查",
            description="充电桩日常维护检查流程"
        )

        # 步骤1: 出发准备
        step1 = TemplateStep(
            id=str(uuid.uuid4()),
            name="出发准备",
            description="准备工具和设备，拍摄出发照片",
            order=1,
            template_id=template1.id
        )
        step1.fields.extend([
            TemplateField(id=str(uuid.uuid4()), name="出发照片", type=FieldType.PHOTO, required=True, step_id=step1.id),
            TemplateField(id=str(uuid.uuid4()), name="出发位置", type=FieldType.LOCATION, required=True, step_id=step1.id),
        ])

        # 步骤2: 到达现场
        step2 = TemplateStep(
            id=str(uuid.uuid4()),
            name="到达现场",
            description="到达站点并记录",
            order=2,
            template_id=template1.id
        )
        step2.fields.extend([
            TemplateField(id=str(uuid.uuid4()), name="到达照片", type=FieldType.PHOTO, required=True, step_id=step2.id),
            TemplateField(id=str(uuid.uuid4()), name="到达位置", type=FieldType.LOCATION, required=True, step_id=step2.id),
            TemplateField(id=str(uuid.uuid4()), name="人脸验证", type=FieldType.FACE_RECOGNITION, required=True, step_id=step2.id),
        ])

        # 步骤3: 设备检查
        step3 = TemplateStep(
            id=str(uuid.uuid4()),
            name="设备检查",
            description="检查充电桩各项功能",
            order=3,
            template_id=template1.id
        )
        step3.fields.extend([
            TemplateField(id=str(uuid.uuid4()), name="外观检查", type=FieldType.TEXT, required=True, step_id=step3.id),
            TemplateField(id=str(uuid.uuid4()), name="电压测量", type=FieldType.NUMBER, required=True, step_id=step3.id),
            TemplateField(id=str(uuid.uuid4()), name="设备照片", type=FieldType.PHOTO, required=True, step_id=step3.id),
        ])

        # 步骤4: 完成工作
        step4 = TemplateStep(
            id=str(uuid.uuid4()),
            name="完成工作",
            description="记录工作结果并签名",
            order=4,
            template_id=template1.id
        )
        step4.fields.extend([
            TemplateField(id=str(uuid.uuid4()), name="工作总结", type=FieldType.TEXT, required=True, step_id=step4.id),
            TemplateField(id=str(uuid.uuid4()), name="完成照片", type=FieldType.PHOTO, required=True, step_id=step4.id),
            TemplateField(id=str(uuid.uuid4()), name="签名", type=FieldType.SIGNATURE, required=True, step_id=step4.id),
        ])

        template1.steps.extend([step1, step2, step3, step4])
        db.add(template1)

        # 提交所有数据
        db.commit()

        print("✅ Database initialized successfully!")
        print("\n📝 Default Users Created:")
        print("   Admin:    admin@igreen.com / admin123")
        print("   Engineer: demo@csenergy.com / demo123")
        print("   Manager:  manager@csenergy.com / manager123")
        print("\n🎉 You can now start the application!")

    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # 首先创建表
    print("📋 Creating database tables...")
    init_db()

    # 然后创建初始数据
    create_initial_data()
