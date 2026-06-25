FROM python:3.12-slim

WORKDIR /app

COPY ai_devops_assistant ./ai_devops_assistant
COPY ai-devops ./ai-devops

ENTRYPOINT ["python", "-m", "ai_devops_assistant.cli"]

