# FastAPI Dev Template

A production-ready FastAPI project template with async PostgreSQL, JWT authentication, role-based access control, and Docker support.

## Features

- **Async-first** — SQLAlchemy 2.0 with asyncpg driver
- **JWT Authentication** — Access & refresh token rotation with OAuth2 password flow
- **Role-Based Access Control** — Scope-based authorization (Guest → Member → Superior → Admin → Developer)
- **Generic CRUD** — Reusable base classes with wildcard query support
- **Docker-ready** — Dev Container for development, Docker Compose for production

## Project Structure

```
.
├── __project_name__/        # Application package (rename this)
│   ├── crud/                # CRUD operations (generic base, user, refresh token)
│   ├── database/            # Async SQLAlchemy engine & session
│   ├── model/               # ORM models (User, RefreshToken)
│   ├── router/              # API route handlers
│   ├── schema/              # Pydantic request/response schemas
│   ├── service/             # Business logic (auth, tokens, passwords)
│   └── system/              # Constants, env config, custom exceptions
├── tests/                   # Test suite
├── main.py                  # Application entry point
├── Dockerfile               # Production container image
├── docker-compose.yml       # Production orchestration
└── .devcontainer/           # VS Code Dev Container config
```

## Getting Started

### 1. Rename the Project Placeholder

This template uses `__project_name__` as a placeholder for the actual project name. Before doing anything else, you **must** replace it across the entire project:

1. **Rename the directory:**
   ```bash
   mv __project_name__ <your_project_name>
   ```

2. **Replace all occurrences in file contents:**
   ```bash
   # Linux / macOS (GNU sed)
   find . -type f -name '*.py' -o -name 'Dockerfile' | xargs sed -i 's/__project_name__/<your_project_name>/g'

   # macOS (BSD sed)
   find . -type f -name '*.py' -o -name 'Dockerfile' | xargs sed -i '' 's/__project_name__/<your_project_name>/g'
   ```

   Files that contain the placeholder include:
   - All Python source files (`import` / `from` statements)
   - `main.py` (app initialization)
   - `Dockerfile` (`COPY` instruction)

### 2. Create the `.env` File

Copy the example and edit it with your own values:

```bash
cp .env.example .env
```

The `.env` file configures the following variables:

| Variable | Required | Default | Description |
|---|---|---|---|
| `POSTGRES_PASSWORD` | **Yes** | — | PostgreSQL password |
| `JWT_SECRET_KEY` | **Yes** | — | Secret key for signing JWTs (generate with `openssl rand -hex 32`) |
| `POSTGRES_USER` | No | `postgres` | PostgreSQL user |
| `POSTGRES_DB` | No | `postgres` | PostgreSQL database name |
| `JWT_ALGORITHM` | No | `HS256` | JWT signing algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | No | `15` | Access token lifetime in minutes |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | No | `7` | Refresh token lifetime in days |

> **Warning:** Never commit your `.env` file. It is already listed in `.gitignore`.

## Development with Dev Container

The recommended development workflow uses [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), which provides a fully configured environment with Python and PostgreSQL out of the box.

### Prerequisites

- [VS Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (`ms-vscode-remote.remote-containers`)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Podman with Docker-compatible CLI)

### Steps

1. Clone the repository and open it in VS Code:
   ```bash
   git clone <repository-url>
   code <repository-directory>
   ```

2. Create your `.env` file as described above.

3. When VS Code detects the `.devcontainer/` directory, it will prompt you to **Reopen in Container**. Click the prompt, or run the command manually:
   - Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Select **Dev Containers: Reopen in Container**

4. VS Code will build the container, install Python dependencies (`pip install -r requirements.txt`), and start a PostgreSQL instance automatically.

5. Start the development server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 5000 --reload
   ```

6. The API is available at `http://localhost:5000`. Interactive docs are at `http://localhost:5000/docs`.

### Included Dev Tools

The Dev Container comes pre-configured with:
- **REST Client** extension for testing API endpoints
- **PostgreSQL** extension for database inspection
- Port forwarding for the app (5000) and PostgreSQL (5432)

## Production Deployment

### Docker

```bash
docker compose up -d --build
```

This starts two services:

| Service | Description | Port |
|---|---|---|
| `app` | FastAPI application (Uvicorn) | 5000 |
| `db` | PostgreSQL 17 | 5432 (internal) |

The database uses a named volume (`postgres-data`) for persistent storage. The app container waits for the database health check to pass before starting.

To stop the services:

```bash
docker compose down
```

To stop and remove all data (including the database volume):

```bash
docker compose down -v
```

### Podman

This project is also compatible with [Podman](https://podman.io/) using `podman-compose`:

```bash
# Install podman-compose if not already available
pip install podman-compose

# Start services
podman-compose up -d --build

# Stop services
podman-compose down
```

> **Note:** If you use Podman with Docker-compatible CLI (`podman-docker`), the standard `docker compose` commands work as-is.

## API Endpoints

All endpoints are under the `/auth` prefix.

| Method | Path | Description | Auth Required |
|---|---|---|---|
| `POST` | `/auth/token` | Sign in (OAuth2 password form) | No |
| `POST` | `/auth/refresh` | Refresh access token | No (refresh token in body) |
| `POST` | `/auth/signup` | Register a new user | No |
| `POST` | `/auth/signout` | Sign out (invalidate refresh token) | Yes |
| `PUT` | `/auth/{user_id}` | Change user access level | Yes (Admin+) |
| `GET` | `/auth/` | List all users | Yes |

## Running Tests

```bash
pytest
```

Tests use an in-memory SQLite database and do not require a running PostgreSQL instance.

## Tech Stack

- **Framework:** FastAPI 0.136
- **Server:** Uvicorn + uvloop
- **Database:** PostgreSQL 17 with SQLAlchemy 2.0 (async)
- **Auth:** PyJWT, Argon2 password hashing (pwdlib)
- **Validation:** Pydantic 2.x
- **Testing:** pytest with anyio (async support)
