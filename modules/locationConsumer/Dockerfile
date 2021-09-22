FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc g++ musl-dev linux-headers geos libc-dev postgresql-dev bash
COPY . .
# COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python","kafka_backburner.py"]