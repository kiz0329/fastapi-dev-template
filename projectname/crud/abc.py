from typing import Type, Generic, TypeVar
from collections.abc import Sequence
import re
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..schema.abc import (
    UploadSchemaBase,
    QuerySchemaBase,
    UserUploadSchemaBase,
    UserQuerySchemaBase,
)
from ..model.abc import DBModelBase, UserModelBase
from ..database import SessionDep
from ..service.password import verify_password, hash_password
from ..system.const import AccessLevel
from ..system.error import (
    ResourceNotFoundError,
    UniqueConstraintError,
    CheckConstraintError,
    ExclusionConstraintError,
    ForeignKeyConstraintError,
    NotNullConstraintError,
)


TModel = TypeVar('TModel', bound=DBModelBase)
TUploadSchema = TypeVar('TUploadSchema', bound=UploadSchemaBase)
TQuerySchema = TypeVar('TQuerySchema', bound=QuerySchemaBase)

TUserModel = TypeVar('TUserModel', bound=UserModelBase)
TUserUploadSchema = TypeVar('TUserUploadSchema', bound=UserUploadSchemaBase)
TUserQuerySchema = TypeVar('TUserQuerySchema', bound=UserQuerySchemaBase)

WILDCARD_REGEX = re.compile(
    r'|'.join([
        r'(?P<escaped_asterisk>\\\*)',
        r'(?P<asterisk>\*)',
        r'(?P<escaped_question>\\\?)',
        r'(?P<question>\?)',
        r'(?P<percent>%)',
        r'(?P<underscore>_)'
    ])
)

DUMMY_PASSWORD_HASH = hash_password("dummy_password")


def _diagnose_integrity_error(e: IntegrityError):
    if getattr(e.orig, "pgcode", None) == "23505":      # Unique violation
        raise UniqueConstraintError(
            f"Resource already exists: {e}")
    elif getattr(e.orig, "pgcode", None) == "23514":    # Check violation
        raise CheckConstraintError(
            f"Check constraint violated: {e}")
    elif getattr(e.orig, "pgcode", None) == "23P01":    # Exclusion violation
        raise ExclusionConstraintError(
            f"Exclusion constraint violated: {e}")
    elif getattr(e.orig, "pgcode", None) == "23503":    # Foreign key violation
        raise ForeignKeyConstraintError(
            f"Foreign key constraint violated: {e}")
    elif getattr(e.orig, "pgcode", None) == "23502":    # Not null violation
        raise NotNullConstraintError(
            f"Not null constraint violated: {e}")
    else:
        # Re-raise the original exception if it's not one of the above
        raise e


class CRUDBase(Generic[TModel, TUploadSchema, TQuerySchema]):
    def __init__(self, model: Type[TModel]):
        self._model = model

    async def create(
            self,
            upload_schema: TUploadSchema,
            db_session: SessionDep) -> TModel:
        obj = self._model(**upload_schema.model_dump())
        db_session.add(obj)
        try:
            await db_session.commit()
        except IntegrityError as e:
            await db_session.rollback()
            _diagnose_integrity_error(e)

        await db_session.refresh(obj)
        return obj

    async def get_list(
            self,
            db_session: SessionDep) -> Sequence[TModel]:
        query = select(self._model)
        result = await db_session.execute(query)
        return result.scalars().all()

    async def query(
            self,
            query_schema: TQuerySchema,
            db_session: SessionDep) -> Sequence[TModel]:
        query = select(self._model)
        query_data = query_schema.model_dump(exclude_none=True)
        for field, value in query_data.items():
            if field.endswith("_pattern"):
                field_name = field[:-8]  # Remove "_pattern" suffix
                query = (
                    query.where(getattr(self._model, field_name).like(
                        _from_glob_to_like(value)))
                )
            elif field.endswith("_from"):
                field_name = field[:-5]  # Remove "_from" suffix
                query = query.where(getattr(self._model, field_name) >= value)
            elif field.endswith("_to"):
                field_name = field[:-3]  # Remove "_to" suffix
                query = query.where(getattr(self._model, field_name) <= value)
            elif field.startswith("undefined_"):
                field_name = field[10:]  # Remove "undefined_" prefix
                query = query.where(getattr(self._model, field_name) == None)
            else:
                query = query.where(getattr(self._model, field) == value)
        result = await db_session.execute(query)
        return result.scalars().all()

    async def get_by_id(
            self,
            id: int,
            db_session: SessionDep) -> TModel:
        result = await db_session.execute(select(self._model).where(self._model.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            raise ResourceNotFoundError(
                f"{self._model.__name__} with id {id} not found")
        return model

    async def update(
            self,
            id: int,
            upload_schema: TUploadSchema,
            db_session: SessionDep) -> TModel:
        obj = await self.get_by_id(id, db_session)
        for field, value in upload_schema.model_dump(exclude_unset=False).items():
            setattr(obj, field, value)
        db_session.add(obj)
        try:
            await db_session.commit()
        except IntegrityError as e:
            await db_session.rollback()
            _diagnose_integrity_error(e)
        await db_session.refresh(obj)
        return obj

    async def delete(
            self,
            id: int,
            db_session: SessionDep) -> TModel:
        obj = await self.get_by_id(id, db_session)
        await db_session.delete(obj)
        try:
            await db_session.commit()
        except IntegrityError as e:
            await db_session.rollback()
            _diagnose_integrity_error(e)
        return obj


def _from_glob_to_like(glob_pattern: str) -> str:
    return WILDCARD_REGEX.sub(lambda m: {
        "escaped_asterisk": "*",
        "asterisk": "%",
        "escaped_question": "?",
        "question": "_",
        "percent": "\\%",
        "underscore": "\\_",
        None: ""
    }[m.lastgroup], glob_pattern)


class UserCRUDBase(CRUDBase[TUserModel, TUserUploadSchema, TUserQuerySchema]):
    async def create(
            self,
            upload_schema: TUserUploadSchema,
            db_session: SessionDep) -> TUserModel:
        hashed_password = hash_password(upload_schema.password)
        upload_data = upload_schema.model_dump(exclude={"password"})
        if isinstance(upload_data.get("access_level"), AccessLevel):
            upload_data["access_level"] = upload_data["access_level"].value
        upload_data["hashed_password"] = hashed_password
        obj = self._model(**upload_data)
        db_session.add(obj)
        try:
            await db_session.commit()
        except IntegrityError as e:
            await db_session.rollback()
            _diagnose_integrity_error(e)

        await db_session.refresh(obj)
        return obj

    async def get_by_username(
            self,
            username: str,
            db_session: SessionDep) -> TUserModel:
        result = await db_session.execute(select(self._model).where(self._model.username == username))
        model = result.scalar_one_or_none()
        if model is None:
            raise ResourceNotFoundError(
                f"{self._model.__name__} with username '{username}' not found"
            )
        return model

    async def get_by_username_and_password(
            self,
            username: str,
            password: str,
            db_session: SessionDep) -> TUserModel:
        resource_not_found = ResourceNotFoundError(
            f"{self._model.__name__} with username '{username}' and provided password not found"
        )
        try:
            model = await self.get_by_username(username, db_session)
        except ResourceNotFoundError:
            # Perform dummy password verification to mitigate timing attacks
            verify_password(password, DUMMY_PASSWORD_HASH)
            raise resource_not_found
        if not verify_password(password, model.hashed_password):
            raise resource_not_found
        return model
