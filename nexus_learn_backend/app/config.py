"""
Configuration settings for Nexus Learn LMS
Modern, secure, and environment-aware configuration
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings with security best practices"""
    
    # Application
    APP_NAME: str = "Nexus Learn"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    ALLOWED_HOSTS: List[str] = Field(
        default=["*"], 
        env="ALLOWED_HOSTS"
    )
    
    # Database
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        env="MONGODB_URL",
        description="MongoDB connection URL"
    )
    DATABASE_NAME: str = Field(
        default="nexus_learn_db",
        env="DATABASE_NAME"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="your-super-secret-key-change-in-production",
        env="SECRET_KEY",
        min_length=32
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_WEBHOOK_URL: Optional[str] = Field(default=None, env="TELEGRAM_WEBHOOK_URL")
    TELEGRAM_ADMIN_IDS: List[int] = Field(default=[], env="TELEGRAM_ADMIN_IDS")
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")
    
    # Features
    ENABLE_REAL_TIME_SYNC: bool = Field(default=True, env="ENABLE_REAL_TIME_SYNC")
    ENABLE_WEBSOCKETS: bool = Field(default=True, env="ENABLE_WEBSOCKETS")
    ENABLE_NOTIFICATIONS: bool = Field(default=True, env="ENABLE_NOTIFICATIONS")
    
    @validator('ALLOWED_HOSTS', pre=True)
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator('TELEGRAM_ADMIN_IDS', pre=True)
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(id.strip()) for id in v.split(",") if id.strip()]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True


def get_settings() -> Settings:
    """Get settings based on environment"""
    return Settings()