"""
SLA Configuration Model
SLA配置模型
"""
from sqlalchemy import Column, String, Integer, Enum
from app.database import Base
from app.models.ticket import Priority


class SLAConfig(Base):
    """
    SLA配置表
    存储不同优先级的响应和解决时间配置
    """
    __tablename__ = "sla_configs"

    id = Column(String(36), primary_key=True, index=True)
    priority = Column(Enum(Priority), nullable=False, unique=True, comment="优先级")
    response_time = Column(Integer, nullable=False, comment="响应时间(分钟)")
    resolution_time = Column(Integer, nullable=False, comment="解决时间(分钟)")

    def __repr__(self):
        return f"<SLAConfig(priority={self.priority}, response_time={self.response_time}, resolution_time={self.resolution_time})>"
