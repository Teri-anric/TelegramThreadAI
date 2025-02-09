"""
Configuration management using Pydantic v2 settings.
"""

import secrets
import logging
from typing import Any
from sqlalchemy import URL
from pydantic import (AmqpDsn, BaseModel, ConfigDict, Field,
                      computed_field, field_validator)
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)



class DatabaseSettings(BaseModel):
    """Database configuration settings."""

    host: str = Field("localhost")
    port: int = Field(5432)
    user: str = Field("postgres")
    password: str = Field("postgres")
    name: str = Field("postgres")

    @property
    def url(self):
        """Construct the full database connection URL."""
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


class RabbitMQSettings(BaseModel):
    """RabbitMQ configuration settings."""

    default_user: str = Field("guest")
    default_pass: str = Field("guest")
    host: str = Field("localhost")
    port: int = Field(5672)
    vhost: str = Field("/")

    @computed_field
    @property
    def url(self) -> AmqpDsn:
        """Construct the full RabbitMQ connection URL."""
        return AmqpDsn.build(
            scheme="amqp",
            username=self.default_user or "guest",
            password=self.default_pass or "guest",
            host=self.host or "localhost",
            port=self.port or 5672,
            path=self.vhost or "/",
        )


class JWTSettings(BaseModel):
    """JWT configuration settings."""

    secret_key: str = Field(
        ...,
        default_factory=lambda: secrets.token_urlsafe(32),
    )
    algorithm: str = Field("HS256")
    access_token_expire_seconds: int = Field(60 * 60 * 24 * 7)  # 1 week


class Settings(BaseSettings):
    """Main application settings."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="_",
    )

    bot_token: str = Field("")
    # can't usage list[str] because of pydantic settings
    cors_origins: Any = Field("")  # type: list[str]  

    # Nested configuration models
    jwt: JWTSettings = JWTSettings()
    database: DatabaseSettings = DatabaseSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()

    @field_validator("cors_origins", mode="before")
    @classmethod
    def decode_cors_origins(cls, v: str) -> list[str]:
        return [x.strip() for x in v.split(",")]


# Create a singleton settings instance
settings = Settings()