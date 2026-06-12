import os as _os

DATABASE_URL = _os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
)
JWT_SECRET_KEY = _os.getenv(
    "JWT_SECRET_KEY",
    "136c78da87d6330ebbf3ed6b06bb2dc3309493850dd64bf80fa4bfa28de1c8ba"
)
JWT_ALGORITHM = _os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(_os.getenv(
    "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    "15"
))
JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(_os.getenv(
    "JWT_REFRESH_TOKEN_EXPIRE_DAYS",
    "7"
))

DEVELOPER_USER_PASSWORD = _os.getenv(
    "DEVELOPER_USER_PASSWORD",
    "pwd"
)
