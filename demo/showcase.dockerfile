# Build image, used to show off Dockerfile colors.
FROM python:3.12-slim AS build
ARG VERSION=2.0.0
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY tools/ ./tools/
RUN pip install --no-cache-dir -r requirements.txt \
    && python tools/generate_themes.py
EXPOSE 8080
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/ || exit 1
CMD ["python", "-m", "http.server", "8080"]
