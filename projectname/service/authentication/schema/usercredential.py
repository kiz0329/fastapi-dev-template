from typing import Annotated, Optional
from pydantic import BaseModel, Field
from .base import QuerySchema, ResponseSchema, UploadSchema
from ..system.const import SHORT_TEXT_LENGTH


class UserCredentialUploadSchema(UploadSchema):
    username: Annotated[
        str,
        Field(
            description="The username of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ]
    password_hash: Annotated[
        str,
        Field(
            description="The hashed password of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ]
    scope: Annotated[
        str,
        Field(
            description="The scope of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ]
    user_id: Annotated[
        Optional[int],
        Field(
            description="The ID of the user associated with the credential"
        )
    ] = None


class UserCredentialQuerySchema(QuerySchema):
    username: Annotated[
        Optional[str],
        Field(
            description="Filter by username of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ] = None
    undefined_user_id: Annotated[
        Optional[int],
        Field(
            description="Filter by user ID associated with the credential"
        )
    ] = None


class UserCredentialResponseSchema(ResponseSchema):
    username: Annotated[
        str,
        Field(
            description="The username of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ]
    password_hash: Annotated[
        str,
        Field(
            description="The hashed password of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ]
    scope: Annotated[
        str,
        Field(
            description="The scope of the user credential",
            max_length=SHORT_TEXT_LENGTH)
    ]
    user_id: Annotated[
        Optional[int],
        Field(
            description="The ID of the user associated with the credential"
        )
    ] = None
