# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py", "--prompt", "test", "--user_id", "demo"]
# Build: docker build -t remix-agent . | Run: docker run -e GEMINI_API_KEY=... remix-agent