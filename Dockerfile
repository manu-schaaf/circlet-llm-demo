FROM python:3.12-bullseye

RUN pip install --no-cache-dir streamlit openai pyyaml

WORKDIR /app
COPY ./src/ /app/

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENV OPENAI_BASE_URL="http://gondor.hucompute.org:11434/v1"

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
