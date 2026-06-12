from typing import Annotated, Optional
from datetime import datetime
from pydantic import Field
from .abc import UploadSchemaBase, ResponseSchemaBase, QuerySchemaBase


class RefreshTokenUploadSchema(UploadSchemaBase):
    token: Annotated[
        str,
        Field(description="The refresh token to be refreshed")
    ]
    expire_at: Annotated[
        datetime,
        Field(description="The expiration time of the refresh token")
    ]
    user_id: Annotated[
        int,
        Field(description="The ID of the user associated with the refresh token")
    ]


class RefreshTokenQuerySchema(QuerySchemaBase):
    token: Annotated[
        Optional[str],
        Field(description="Filter by the refresh token to be refreshed")
    ] = None
    expire_at_from: Annotated[
        Optional[datetime],
        Field(description="Filter by the start of the expiration time range for refresh tokens")
    ] = None
    expire_at_to: Annotated[
        Optional[datetime],
        Field(
            description="Filter by the end of the expiration time range for refresh tokens")
    ] = None


class RefreshTokenResponseSchema(ResponseSchemaBase):
    token: Annotated[
        str,
        Field(description="The refresh token to be refreshed")
    ]
    expire_at: Annotated[
        datetime,
        Field(description="The expiration time of the refresh token")
    ]
    user_id: Annotated[
        int,
        Field(description="The ID of the user associated with the refresh token")
    ]
