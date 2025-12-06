FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy files
COPY . .

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root
   
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
