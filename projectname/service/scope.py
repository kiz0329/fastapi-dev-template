from ..system.const import AccessLevel


def generate_access_level_scopes(access_level: AccessLevel) -> list[str]:
    scopes = list[str]()
    if access_level.value >= AccessLevel.GUEST.value:
        scopes.append(get_access_level_scope(AccessLevel.GUEST))
    if access_level.value >= AccessLevel.MEMBER.value:
        scopes.append(get_access_level_scope(AccessLevel.MEMBER))
    if access_level.value >= AccessLevel.SUPERIOR.value:
        scopes.append(get_access_level_scope(AccessLevel.SUPERIOR))
    if access_level.value >= AccessLevel.ADMIN.value:
        scopes.append(get_access_level_scope(AccessLevel.ADMIN))
    if access_level.value >= AccessLevel.DEVELOPER.value:
        scopes.append(get_access_level_scope(AccessLevel.DEVELOPER))
    return scopes


def get_access_level_scope(access_level: AccessLevel) -> str:
    return (
        "guest" if access_level.value == AccessLevel.GUEST.value else
        "member" if access_level.value == AccessLevel.MEMBER.value else
        "superior" if access_level.value == AccessLevel.SUPERIOR.value else
        "admin" if access_level.value == AccessLevel.ADMIN.value else
        "developer" if access_level.value == AccessLevel.DEVELOPER.value else
        "none"
    )
