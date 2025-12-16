"""
Problem Type Model
问题类型模型
"""
from sqlalchemy import Column, String, Text

from app.database import Base


class ProblemType(Base):
    """
    问题类型表
    存储可用的问题类型
    """
    __tablename__ = "problem_types"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, comment="问题类型名称")
    description = Column(Text, nullable=True, comment="问题类型描述")

    def __repr__(self):
        return f"<ProblemType(id={self.id}, name={self.name})>"
