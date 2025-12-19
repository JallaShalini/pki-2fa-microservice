# Multi-stage build for PKI-based 2FA microservice

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set timezone to UTC
ENV TZ=UTC
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy key files
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Set up cron job
RUN chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron && \
    touch /var/log/cron.log

# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose port
EXPOSE 8080

# Start cron and application
CMD cron && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080
