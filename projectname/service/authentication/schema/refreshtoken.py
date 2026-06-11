from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field
from .base import QuerySchema, ResponseSchema, UploadSchema
from ..system.const import SHORT_TEXT_LENGTH


class RefreshTokenUploadSchema(UploadSchema):
    token: Annotated[
        str,
        Field(
            description="The refresh token string",
            max_length=SHORT_TEXT_LENGTH
        ),
    ]
    expires_at: Annotated[
        datetime,
        Field(description="The expiration time of the refresh token")
    ]
    user_credential_id: Annotated[
        int,
        Field(description="The ID of the user credential associated with the refresh token")
    ]


class RefreshTokenQuerySchema(QuerySchema):
    token: Annotated[
        Optional[str],
        Field(description="Filter by refresh token string")
    ] = None
    expires_at_to: Annotated[
        Optional[datetime],
        Field(description="Filter by refresh token expiration time (to)")
    ] = None
    expires_at_from: Annotated[
        Optional[datetime],
        Field(description="Filter by refresh token expiration time (from)")
    ] = None
    user_credential_id: Annotated[
        Optional[int],
        Field(description="Filter by user credential ID associated with the refresh token")
    ] = None


class RefreshTokenResponseSchema(ResponseSchema):
    token: Annotated[
        str,
        Field(description="The refresh token string")
    ]
    expires_at: Annotated[
        datetime,
        Field(description="The expiration time of the refresh token")
    ]
    user_credential_id: Annotated[
        int,
        Field(description="The ID of the user credential associated with the refresh token")
    ]
