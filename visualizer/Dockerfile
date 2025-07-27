FROM python:3.11

WORKDIR /app

COPY visualization.py .

RUN pip install dash pandas sqlalchemy "psycopg[binary]"

CMD ["python", "visualization.py"]