import logging
import os
from kafka import KafkaConsumer
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CREATE_LOCATION_TOPIC = os.environ["CREATE_LOCATION_TOPIC"]
logger.info('Kafka started listening topic: {} '.format(CREATE_LOCATION_TOPIC))
KAFKA_BS_NAME = os.environ["KAFKA_BS_NAME"]
KAFKA_BS_PORT = os.environ["KAFKA_BS_PORT"]

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

KAFKA_SERVER = '{}:{}'.format(KAFKA_BS_NAME, KAFKA_BS_PORT)
consumer = KafkaConsumer(CREATE_LOCATION_TOPIC, bootstrap_servers=KAFKA_SERVER)

def save_to_db(location):
    # CCB to do bulk inserts.
    from sqlalchemy import create_engine

    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    conn = engine.connect()

    person_id = int(location["person_id"])
    latitude, longitude = int(location["latitude"]), int(location["longitude"])

    insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))" \
        .format(person_id, latitude, longitude)

    logger.info("Created new location for person_id: {}".format(person_id))
    conn.execute(insert)

loop = True
while loop:
    try: 
        logger.info("Polling from Topic: {}".format(CREATE_LOCATION_TOPIC))
        message = consumer.poll(10.0)

        if not message:
            time.sleep(10)
        else:
            for k, messages in message.items():
                for msg in messages:
                    msg_str = msg.value.decode('utf-8')
                    msg_json =json.loads(msg_str)
                    save_to_db(msg_json)

    except Exception as e:
        logger.error(str(e))
        loop = False
