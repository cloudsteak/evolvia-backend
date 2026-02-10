FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set workdir
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies system-wide (no venv)
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application files
COPY . .
   
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
