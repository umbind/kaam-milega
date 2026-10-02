# Production Dockerfile for "काम मिलेगा" (Kaam Milega)
# Lightweight, hardened, non-root async container

FROM python:3.10-slim

# Set environment flags for optimal container execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8080

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for OWASP container security
RUN useradd -m -u 1001 kaamuser && \
    chown -R kaamuser:kaamuser /app

# Copy application source code
COPY --chown=kaamuser:kaamuser . .

# Switch to non-root user
USER kaamuser

# Expose service port
EXPOSE 8080

# Health check to ensure zero-downtime orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/stats').read()" || exit 1

# Start the async server
CMD ["python", "server.py"]
