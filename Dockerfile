# Nexus Learn - Unified Dockerfile for Render Deployment
# Serves both FastAPI backend and static frontend files

FROM python:3.11-slim

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        ffmpeg \
        libmagic1 \
        poppler-utils \
        nginx-light \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY nexus_learn_backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY nexus_learn_backend/app/ /app/app/

# Copy frontend files
COPY frontend/ /app/frontend/
COPY static/ /app/static/

# Create necessary directories
RUN mkdir -p /app/uploads /app/temp /app/logs

# Create a unified FastAPI app that serves both API and frontend
COPY main.py /app/main.py

# Create nginx config for production optimization (optional)
COPY nginx.conf /etc/nginx/sites-available/default

# Create supervisor config for running multiple services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create non-root user
RUN adduser --disabled-password --gecos '' --uid 1000 appuser \
    && chown -R appuser:appuser /app \
    && chown -R appuser:appuser /var/log/nginx \
    && chown -R appuser:appuser /var/lib/nginx

# Switch to non-root user
USER appuser

# Expose port (Render will automatically bind to this)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the unified application
CMD ["python", "main.py"]
