from enum import Enum as _Enum, auto as _auto


class AccessLevel(_Enum):
    GUEST = _auto()
    MEMBER = _auto()
    SUPERIOR = _auto()
    ADMIN = _auto()
    DEVELOPER = _auto()


GUEST_SCOPE = "guest"
MEMBER_SCOPE = "member"
SUPERIOR_SCOPE = "superior"
ADMIN_SCOPE = "admin"
DEVELOPER_SCOPE = "developer"


SHORT_TEXT_LENGTH = 255
DEVELOPER_USER_NAME = "developer"