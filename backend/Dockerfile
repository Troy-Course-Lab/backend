# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables for Python and uv
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app

# Set the working directory
WORKDIR /app/

# Install uv - a fast Python package installer
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# --- MODIFICATION START ---
# This section is corrected to use the proper file paths.

# 1. Copy only the files needed for dependency installation from the backend/ directory.
COPY backend/pyproject.toml backend/uv.lock ./

# 2. Install dependencies.
RUN uv sync --frozen --no-install-project

# 3. Copy the rest of the backend application code, not the whole repository.
COPY backend/ .

# 4. Install the project itself into the virtual environment.
RUN uv sync

# --- MODIFICATION END ---

COPY backend/docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh
# Set the command to run the application
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]