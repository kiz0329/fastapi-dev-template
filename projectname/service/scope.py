from ..system.const import (
    AccessLevel,
    GUEST_SCOPE,
    MEMBER_SCOPE,
    SUPERIOR_SCOPE,
    ADMIN_SCOPE,
    DEVELOPER_SCOPE,
)


def generate_access_level_scopes(access_level: AccessLevel) -> list[str]:
    scopes = list[str]()
    if access_level.value >= AccessLevel.GUEST.value:
        scopes.append(GUEST_SCOPE)
    if access_level.value >= AccessLevel.MEMBER.value:
        scopes.append(MEMBER_SCOPE)
    if access_level.value >= AccessLevel.SUPERIOR.value:
        scopes.append(SUPERIOR_SCOPE)
    if access_level.value >= AccessLevel.ADMIN.value:
        scopes.append(ADMIN_SCOPE)
    if access_level.value >= AccessLevel.DEVELOPER.value:
        scopes.append(DEVELOPER_SCOPE)
    return scopes
