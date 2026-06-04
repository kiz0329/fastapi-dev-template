from typing import Annotated, Optional
from pydantic import Field, ConfigDict
from .base import UploadSchema, ResponseSchema, QuerySchema


class UserCredentialUploadSchema(UploadSchema):
    username: Annotated[
        str,
        Field(description="The username of the user credential")
    ]
    password_hash: Annotated[
        str,
        Field(description="The hashed password of the user credential")
    ]


class UserCredentialResponseSchema(ResponseSchema):
    username: Annotated[
        str,
        Field(description="The username of the user credential")
    ]
    disabled: Annotated[
        bool,
        Field(description="Indicates whether the user credential is disabled")
    ]


class UserCredentialQuerySchema(QuerySchema):
    username: Annotated[
        Optional[str],
        Field(description="Filter user credentials by username")
    ] = None
    disabled: Annotated[
        Optional[bool],
        Field(description="Filter user credentials by disabled status")
    ] = None


class UserCredentialInDBSchema(UserCredentialResponseSchema):
    username: Annotated[
        str,
        Field(description="The username of the user credential")
    ]
    password_hash: Annotated[
        str,
        Field(description="The hashed password of the user credential")
    ]
    disabled: Annotated[
        bool,
        Field(description="Indicates whether the user credential is disabled")
    ]

    model_config = ConfigDict(from_attributes=True)
