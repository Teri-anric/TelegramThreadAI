"""
Configuration management using Pydantic v2 settings.
"""

from typing import Optional
import secrets

from pydantic import BaseModel, PostgresDsn, AmqpDsn, Field, ConfigDict, computed_field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    """Database configuration settings."""

    host: str = Field("localhost")
    port: str = Field("5432")
    user: str = Field("postgres")
    password: str = Field("postgres")
    name: str = Field("postgres")

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        """Construct the full database connection URL."""
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )


class RabbitMQSettings(BaseModel):
    """RabbitMQ configuration settings."""

    default_user: str = Field("guest")
    default_pass: str = Field("guest")
    host: str = Field("localhost")
    port: str = Field("5672")
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
    cors_origins: list[str] = Field([])

    # Nested configuration models
    jwt: JWTSettings = JWTSettings()
    database: DatabaseSettings = DatabaseSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()


# Create a singleton settings instance
settings = Settings()
