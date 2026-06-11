from typing import Annotated, Optional
from datetime import datetime
from ..system.const import AccessLevel
from pydantic import BaseModel, ConfigDict, Field


class UploadSchemaBase(BaseModel):
    pass


class ResponseSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[
        int,
        Field(description="The unique identifier of the object")]
    created_at: Annotated[
        datetime,
        Field(description="The timestamp of the creation")]
    updated_at: Annotated[
        datetime,
        Field(description="The timestamp of the last update")]


class QuerySchemaBase(BaseModel):
    created_at_from: Annotated[
        Optional[datetime],
        Field(description="Filter objects created after this timestamp")
    ] = None
    created_at_to: Annotated[
        Optional[datetime],
        Field(description="Filter objects created before this timestamp")
    ] = None
    updated_at_from: Annotated[
        Optional[datetime],
        Field(description="Filter objects updated after this timestamp")
    ] = None
    updated_at_to: Annotated[
        Optional[datetime],
        Field(description="Filter objects updated before this timestamp")
    ] = None


class UserUploadSchemaBase(UploadSchemaBase):
    username: Annotated[
        str,
        Field(description="The unique username for authentication")
    ]
    password: Annotated[
        str,
        Field(description="The password for authentication")
    ]
    access_level: Annotated[
        AccessLevel,
        Field(description="The access level for the user", default=AccessLevel.GUEST)
    ]


class UserResponseSchemaBase(ResponseSchemaBase):
    username: Annotated[
        str,
        Field(description="The unique username for authentication")
    ]
    hashed_password: Annotated[
        str,
        Field(description="The hashed password for authentication")
    ]
    access_level: Annotated[
        AccessLevel,
        Field(description="The access level for the user")
    ]


class UserQuerySchemaBase(QuerySchemaBase):
    username: Annotated[
        Optional[str],
        Field(description="Filter users by username for authentication")
    ] = None
