from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from app.web.api.shemas.api import ApiResponse
from app.web.api.shemas.user import UserSchema


class TelegramLoginWidgetCredentials(BaseModel):
    """
    Telegram login widget credentials schema.

    :note: All extra fields are allowed.
    """

    model_config = ConfigDict(extra="allow")

    id: int = Field(..., description="Unique identifier for the user.")
    first_name: str = Field(..., description="First name of the user.")
    last_name: str | None = Field(None, description="Last name of the user.")
    username: str | None = Field(None, description="Username of the user.")
    photo_url: str | None = Field(None, description="URL of the user's photo.")
    hash: str = Field(..., description="Hash for verification.")


class TelegramLoginWidgetLoginData(BaseModel):
    """
    Telegram login widget login data schema.
    """

    credentials: TelegramLoginWidgetCredentials = Field(
        ..., description="Credentials for the Telegram login widget."
    )
    login_type: Literal["tg_login_widget"] = Field(
        ..., description="Type of login, defaults to 'tg_login_widget'."
    )


LoginData = Union[TelegramLoginWidgetLoginData]
"""
Login data schema.
"""


class LoginResponse(ApiResponse):
    """
    Login response schema.
    """

    user: UserSchema | None = Field(None, description="User information.")
    access_token: str | None = Field(None, description="Access token for the session.")
