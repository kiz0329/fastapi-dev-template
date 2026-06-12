from typing import Annotated
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: Annotated[
        str,
        Field(description="The access token string")
    ]
    refresh_token: Annotated[
        str,
        Field(description="The refresh token string")
    ]
    token_type: Annotated[
        str,
        Field(description="The type of the token, typically 'bearer'",
              default="bearer")
    ] = "bearer"


class RefreshToken(BaseModel):
    token: Annotated[
        str,
        Field(description="The refresh token string")
    ]
