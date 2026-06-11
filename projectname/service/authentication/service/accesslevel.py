from ..system.const import (
    AccessLevel,
    GUEST_ACCESS_SCOPE,
    MEMBER_ACCESS_SCOPE,
    SUPERIOR_ACCESS_SCOPE,
    ADMIN_ACCESS_SCOPE,
    DEVELOPER_ACCESS_SCOPE,
)


def provide_access_level_scope_str(access_level: AccessLevel) -> str:
    scopes = list[str]()
    if access_level.value >= AccessLevel.GUEST.value:
        scopes.append(GUEST_ACCESS_SCOPE)
    if access_level.value >= AccessLevel.MEMBER.value:
        scopes.append(MEMBER_ACCESS_SCOPE)
    if access_level.value >= AccessLevel.SUPERIOR.value:
        scopes.append(SUPERIOR_ACCESS_SCOPE)
    if access_level.value >= AccessLevel.ADMIN.value:
        scopes.append(ADMIN_ACCESS_SCOPE)
    if access_level.value >= AccessLevel.DEVELOPER.value:
        scopes.append(DEVELOPER_ACCESS_SCOPE)
    return " ".join(scopes)
