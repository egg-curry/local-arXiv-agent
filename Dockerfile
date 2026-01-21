FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install -U pip streamlit requests weaviate-client ollama
ENV STREAMLIT_SERVER_PORT=8502 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

EXPOSE 8502
ENTRYPOINT ["streamlit", "run", "app_streamlit.py", "--server.port=8502", "--server.address=0.0.0.0"]
