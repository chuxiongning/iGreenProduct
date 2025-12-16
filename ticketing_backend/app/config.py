"""
Application Configuration
从环境变量加载配置
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用程序设置"""

    # Database Configuration
    # MySQL数据库连接配置
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = "igreen_user"
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = "igreen_ticketing"

    # Database Type (mysql or sqlite)
    DATABASE_TYPE: str = "sqlite"  # Change to "mysql" for production

    @property
    def DATABASE_URL(self) -> str:
        """构建数据库连接URL"""
        if self.DATABASE_TYPE == "sqlite":
            return "sqlite:///./igreen_ticketing.db"
        else:
            return f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Application Configuration
    APP_NAME: str = "iGreen Ticketing System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB

    # CORS Configuration
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def ALLOWED_ORIGINS_LIST(self) -> List[str]:
        """将CORS origins转换为列表"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # Face Recognition (optional)
    FACE_RECOGNITION_API_URL: str = ""
    FACE_RECOGNITION_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局设置实例
settings = Settings()
