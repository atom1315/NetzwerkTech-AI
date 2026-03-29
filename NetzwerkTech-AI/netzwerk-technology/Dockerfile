FROM python:3.12-slim AS base

LABEL maintainer="NetzwerkTech Team"
LABEL description="NetzwerkTech AI — KI-gestützte Netzwerk-Analyse"

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[all]" 2>/dev/null || pip install --no-cache-dir .

# Application code
COPY src/ src/
COPY examples/ examples/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import src; print('OK')" || exit 1

EXPOSE 8080

CMD ["uvicorn", "src.ai_network_analyzer.engine:app", "--host", "0.0.0.0", "--port", "8080"]
