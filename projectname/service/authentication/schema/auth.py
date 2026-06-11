from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field
from ..system.const import SHORT_TEXT_LENGTH


class Sign(BaseModel):
    username: Annotated[
        str,
        Field(
            description="The username of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ]
    password: Annotated[
        str,
        Field(
            description="The password of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ]


class Token(BaseModel):
    access_token: Annotated[
        str,
        Field(description="JWT access token")
    ]
    refresh_token: Annotated[
        str,
        Field(description="Refresh token")
    ]
    token_type: Annotated[
        str,
        Field(description="Type of the token, typically 'Bearer'")
    ] = "Bearer"


class RefreshToken(BaseModel):
    refresh_token: Annotated[
        str,
        Field(description="Refresh token")
    ]
