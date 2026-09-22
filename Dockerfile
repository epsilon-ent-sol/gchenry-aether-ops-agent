# Multi-stage Python 3.11 build optimized for Cloud Run
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
# Copy installed dependencies
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Non-root security best practice
RUN useradd -u 8888 aether
USER aether

COPY --chown=aether:aether . .

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

