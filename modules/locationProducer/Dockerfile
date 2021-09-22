FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc g++ musl-dev linux-headers geos libc-dev postgresql-dev bash
COPY . .

RUN chmod -R 755 start_server.sh
# COPY requirements.txt requirements.txt
RUN pip install grpcio-1.40.0-cp37-cp37m-linux_x86_64.whl
RUN pip install grpcio_tools-1.40.0-cp37-cp37m-linux_x86_64.whl
RUN pip install -r requirements.txt

EXPOSE 50051

CMD ["./start_server.sh"]