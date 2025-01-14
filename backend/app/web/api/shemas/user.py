from pydantic import BaseModel, ConfigDict
from typing import Literal, Union


class UserSchema(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )
    
    id: int
    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None


class TelegramLoginWidgetCredentials(BaseModel):
    model_config = ConfigDict(
        extra='allow'
    )
    
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    hash: str


class TelegramLoginWidgetLoginData(BaseModel):
    credentials: TelegramLoginWidgetCredentials
    login_type: Literal["tg_login_widget"] = "tg_login_widget"

LoginData = Union[TelegramLoginWidgetLoginData]


class LoginResponse(BaseModel):
    status: Literal["ok", "error"]
    message: str | None = None
    user: UserSchema | None = None
    access_token: str | None = None