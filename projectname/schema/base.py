from typing import Annotated, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class UploadSchema(BaseModel):
    pass


class ResponseSchema(BaseModel):
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


class QuerySchema(BaseModel):
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
