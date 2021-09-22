import locationEvent_pb2
import locationEvent_pb2_grpc
import grpc
import json
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from concurrent import futures
from kafka import KafkaProducer

KAFKA_BS_NAME = os.environ["KAFKA_BS_NAME"]
KAFKA_BS_PORT = os.environ["KAFKA_BS_PORT"]
CREATE_LOCATION_TOPIC = "create_location" #os.environ["CREATE_LOCATION_TOPIC"]
KAFKA_SERVER = '{}:{}'.format(KAFKA_BS_NAME, KAFKA_BS_PORT)
logging.info("Connecting to Kafka server: {}".format(KAFKA_SERVER))
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


class EventCoordinatesService(locationEvent_pb2_grpc.EventCoordinatesServiceServicer):

    def Create(self, request, context):
        request_value = {
            'personId': int(request.personId),
            'latitude': int(request.latitude),
            'longitude': int(request.longitude)
        }
        new_location  = json.dumps(request_value).encode('utf-8')
        producer.send(CREATE_LOCATION_TOPIC, new_location)
        logging.info("Sending data to Kafka: {}".format(request_value))
        return locationEvent_pb2.EventCoordinatesMessage(**request_value)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
locationEvent_pb2_grpc.add_EventCoordinatesServiceServicer_to_server(EventCoordinatesService(), server)

logging.info('starting gRPC server: 50051')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()