# Evolvia Lab management backend service. 


## Pre-requisites

Python 3.13

## Setup

### Create virtual environment with uv

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create Python 3.13 virtual environment
uv venv --python 3.13

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Sync dependencies (includes lock file generation)
uv sync

# Or manually install dependencies
# uv pip install fastapi uvicorn[standard] redis python-dotenv ...
```

## Run

```bash
uvicorn main:app --reload
```
