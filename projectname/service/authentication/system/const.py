from enum import Enum as _Enum, auto as _auto
from ....system.const import SHORT_TEXT_LENGTH


class AccessLevel(_Enum):
    GUEST = _auto()
    MEMBER = _auto()
    SUPERIOR = _auto()
    ADMIN = _auto()
    DEVELOPER = _auto()


GUEST_ACCESS_SCOPE = "guest"
MEMBER_ACCESS_SCOPE = "member"
SUPERIOR_ACCESS_SCOPE = "superior"
ADMIN_ACCESS_SCOPE = "admin"
DEVELOPER_ACCESS_SCOPE = "developer"
