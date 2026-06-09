from typing import Annotated, Optional
from pydantic import Field
from .base import UploadSchema, ResponseSchema, QuerySchema


class UserUploadSchema(UploadSchema):
    first_name: Annotated[
        str,
        Field(description="The first name of the user")
    ]
    last_name: Annotated[
        str,
        Field(description="The last name of the user")
    ]


class UserResponseSchema(ResponseSchema):
    first_name: Annotated[
        str,
        Field(description="The first name of the user")
    ]
    last_name: Annotated[
        str,
        Field(description="The last name of the user")
    ]


class UserQuerySchema(QuerySchema):
    first_name: Annotated[
        Optional[str],
        Field(description="Filter users by first name")
    ] = None
    last_name: Annotated[
        Optional[str],
        Field(description="Filter users by last name")
    ] = None
