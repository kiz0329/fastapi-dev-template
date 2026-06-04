from typing import Annotated, Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: Annotated[
        str,
        Field(description="The access token")
    ]
    refresh_token: Annotated[
        str,
        Field(description="The refresh token")
    ]
    token_type: Annotated[
        str,
        Field(description="The type of the token")
    ] = "bearer"


class TokenData(BaseModel):
    username: Annotated[
        str,
        Field(description="The username contained in the token, typically usercredential id is used as username")
    ]
    scopes: Annotated[
        list[str],
        Field(description="The scopes contained in the token")
    ] = []
