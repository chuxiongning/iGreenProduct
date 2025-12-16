"""
Site Level Configuration Model
站点级别配置模型
"""
from sqlalchemy import Column, String, Text, Float

from app.database import Base


class SiteLevelConfig(Base):
    """
    站点级别配置表
    存储不同站点级别的配置信息(如SLA倍数等)
    """
    __tablename__ = "site_level_configs"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, comment="站点级别名称")
    description = Column(Text, nullable=True, comment="描述")
    sla_multiplier = Column(Float, nullable=False, default=1.0, comment="SLA时间倍数")

    def __repr__(self):
        return f"<SiteLevelConfig(id={self.id}, name={self.name}, sla_multiplier={self.sla_multiplier})>"
