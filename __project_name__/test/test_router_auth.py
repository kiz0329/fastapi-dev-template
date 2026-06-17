import uuid
import pytest
from fastapi import HTTPException

from __project_name__.router.auth import sign_in, refresh_token, sign_out, sign_up, change_access_level, get_users
from __project_name__.schema.token import RefreshToken as RefreshTokenSchema
from __project_name__.schema.user import UserUploadSchema
from __project_name__.service.token import TokenData
from __project_name__.system.const import AccessLevel, DEVELOPER_USER_NAME
from __project_name__.system.error import UniqueConstraintError


def _unique_user(prefix: str = "user") -> UserUploadSchema:
    return UserUploadSchema(username=f"{prefix}_{uuid.uuid4().hex[:8]}", password="pass123", first_name="F", last_name="L")


# --- sign_in ---


@pytest.mark.anyio
async def test_sign_in(developer_user, db_session):
    result = await sign_in(developer_user, db_session)
    assert result.token_type == "bearer"
    assert result.access_token
    assert result.refresh_token


# --- refresh_token ---


@pytest.mark.anyio
async def test_refresh_token(developer_user, db_session):
    tokens = await sign_in(developer_user, db_session)
    result = await refresh_token(RefreshTokenSchema(token=tokens.refresh_token), db_session)
    assert result.access_token
    assert result.refresh_token != tokens.refresh_token


@pytest.mark.anyio
async def test_refresh_token_invalid(db_session):
    with pytest.raises(HTTPException) as exc:
        await refresh_token(RefreshTokenSchema(token="invalid_token"), db_session)
    assert exc.value.status_code == 401


# --- sign_up ---


@pytest.mark.anyio
async def test_sign_up(db_session):
    schema = _unique_user("signup")
    result = await sign_up(schema, db_session)
    assert result.username == schema.username
    assert result.first_name == "F"


@pytest.mark.anyio
async def test_sign_up_duplicate(db_session):
    schema = _unique_user("dup")
    await sign_up(schema, db_session)
    with pytest.raises(UniqueConstraintError):
        await sign_up(schema, db_session)


# --- sign_out ---


@pytest.mark.anyio
async def test_sign_out(developer_user, developer_token_data, db_session):
    tokens = await sign_in(developer_user, db_session)
    result = await sign_out(RefreshTokenSchema(token=tokens.refresh_token), db_session, developer_token_data)
    assert result.username == DEVELOPER_USER_NAME


@pytest.mark.anyio
async def test_sign_out_wrong_owner(developer_user, db_session):
    tokens = await sign_in(developer_user, db_session)
    wrong_token_data = TokenData(username="other_user", scopes=[])
    with pytest.raises(HTTPException) as exc:
        await sign_out(RefreshTokenSchema(token=tokens.refresh_token), db_session, wrong_token_data)
    assert exc.value.status_code == 401


# --- change_access_level ---


@pytest.mark.anyio
async def test_change_access_level(developer_token_data, db_session):
    new_user = await sign_up(_unique_user("level"), db_session)
    result = await change_access_level(new_user.id, AccessLevel.MEMBER, developer_token_data, db_session)
    assert result.access_level == AccessLevel.MEMBER.value


@pytest.mark.anyio
async def test_change_access_level_not_found(developer_token_data, db_session):
    with pytest.raises(HTTPException) as exc:
        await change_access_level(99999, AccessLevel.MEMBER, developer_token_data, db_session)
    assert exc.value.status_code == 404


# --- get_users ---


@pytest.mark.anyio
async def test_get_users(developer_token_data, db_session):
    result = await get_users(developer_token_data, db_session)
    assert isinstance(result, list)
    assert any(u.username == DEVELOPER_USER_NAME for u in result)
