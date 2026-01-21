FROM python:3.12-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN pip install --no-cache-dir uv
RUN pip install --no-cache-dir streamlit
RUN pip install --no-cache-dir weaviate-client
WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN pip install --no-cache-dir uv streamlit weaviate-client && \
    uv sync --frozen && \
    chown -R appuser:appuser /app

USER appuser
COPY --chown=appuser:appuser . .

EXPOSE 8501
CMD ["streamlit", "run", "ui/app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
