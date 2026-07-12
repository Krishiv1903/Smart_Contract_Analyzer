# ==========================================================
# Legal Knowledge Graph
# Dockerfile
# ==========================================================

FROM python:3.13-slim

# ----------------------------------------------------------
# Environment
# ----------------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------------------------------------
# Working Directory
# ----------------------------------------------------------

WORKDIR /app

# ----------------------------------------------------------
# Install system dependencies
# ----------------------------------------------------------

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------
# Install Python packages
# ----------------------------------------------------------

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------
# Download spaCy model
# ----------------------------------------------------------

RUN python -m spacy download en_core_web_sm

# ----------------------------------------------------------
# Copy Project
# ----------------------------------------------------------

COPY . .

# ----------------------------------------------------------
# Create runtime directories
# ----------------------------------------------------------

RUN mkdir -p \
    logs \
    output/json \
    output/html \
    output/graphs

# ----------------------------------------------------------
# Run application
# ----------------------------------------------------------

CMD ["python", "main.py"]