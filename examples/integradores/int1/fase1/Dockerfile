FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir flask psycopg2-binary
COPY app.py /app/app.py
EXPOSE 5000
CMD ["python", "app.py"]