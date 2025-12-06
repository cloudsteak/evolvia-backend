FROM python:3.13-slim

RUN pip install --upgrade pip
# Install Poetry
RUN pip install poetry

# Set workdir
WORKDIR /app

# Copy files
COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root
   
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
