from typing import Annotated, Optional
from pydantic import Field
from .abc import UploadSchema, ResponseSchema, QuerySchema


class UserUploadSchema(UploadSchema):
    username: Annotated[
        str,
        Field(description="The unique username for authentication")
    ]
    hashed_password: Annotated[
        str,
        Field(description="The hashed password for authentication")
    ]
    first_name: Annotated[
        str,
        Field(description="The first name of the user")
    ]
    last_name: Annotated[
        str,
        Field(description="The last name of the user")
    ]


class UnhashedUserUploadSchema(UploadSchema):
    username: Annotated[
        str,
        Field(description="The unique username for authentication")
    ]
    password: Annotated[
        str,
        Field(description="The unhashed password for authentication")
    ]
    first_name: Annotated[
        str,
        Field(description="The first name of the user")
    ]
    last_name: Annotated[
        str,
        Field(description="The last name of the user")
    ]


class UserQuerySchema(QuerySchema):
    username: Annotated[
        Optional[str],
        Field(description="Filter users by username for authentication")
    ] = None
    first_name: Annotated[
        Optional[str],
        Field(description="Filter users by first name")
    ] = None
    last_name: Annotated[
        Optional[str],
        Field(description="Filter users by last name")
    ] = None


class UserResponseSchema(ResponseSchema):
    username: Annotated[
        str,
        Field(description="The unique username for authentication")
    ]
    first_name: Annotated[
        str,
        Field(description="The first name of the user")
    ]
    last_name: Annotated[
        str,
        Field(description="The last name of the user")
    ]
