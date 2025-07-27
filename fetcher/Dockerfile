FROM python:3.11

WORKDIR /app

COPY fetch_countries_only_async.py .

RUN pip install aiohttp pandas sqlalchemy psycopg2-binary openpyxl

CMD ["python", "fetch_countries_only_async.py"]