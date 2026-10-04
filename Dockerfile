FROM python:3.11-slim

LABEL description="Win2000 Agent - pure stdlib AI research agent"

WORKDIR /app
COPY win2000_agent.py .

ENV BACKEND=zhipu
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "win2000_agent.py"]
CMD ["solid state battery"]