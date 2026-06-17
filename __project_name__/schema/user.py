from typing import Annotated, Optional
from pydantic import Field
from .abc import UserUploadSchemaBase, UserResponseSchemaBase, UserQuerySchemaBase


class UserUploadSchema(UserUploadSchemaBase):
    first_name: Annotated[
        str,
        Field(description="The first name of the user")
    ]
    last_name: Annotated[
        str,
        Field(description="The last name of the user")
    ]


class UserQuerySchema(UserQuerySchemaBase):
    first_name: Annotated[
        Optional[str],
        Field(description="Filter users by first name")
    ] = None
    last_name: Annotated[
        Optional[str],
        Field(description="Filter users by last name")
    ] = None


class UserResponseSchema(UserResponseSchemaBase):
    first_name: Annotated[
        str,
        Field(description="The first name of the user")
    ]
    last_name: Annotated[
        str,
        Field(description="The last name of the user")
    ]
