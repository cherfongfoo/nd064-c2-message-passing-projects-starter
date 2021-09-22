import os
from typing import List, Type

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

KAFKA_BS_NAME = os.environ["KAFKA_BS_NAME"]
CREATE_LOCATION_TOPIC = os.environ["CREATE_LOCATION_TOPIC"]
KAFKA_BS_PORT = os.environ["KAFKA_BS_PORT"]
KAFKA_BROKER_LIST_NAME = os.environ["KAFKA_BROKER_LIST_NAME"]
KAFKA_BROKER_PORT = os.environ["KAFKA_BROKER_PORT"]

class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    KAFKA_BS_NAME = os.environ["KAFKA_BS_NAME"]
    CREATE_PERSON_TOPIC = os.environ["CREATE_PERSON_TOPIC"]
    CREATE_LOCATION_TOPIC = os.environ["CREATE_LOCATION_TOPIC"]
    KAFKA_BS_PORT = os.environ["KAFKA_BS_PORT"]
    KAFKA_BROKER_LIST_NAME = os.environ["KAFKA_BROKER_LIST_NAME"]
    KAFKA_BROKER_PORT = os.environ["KAFKA_BROKER_PORT"]

class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    SECRET_KEY = os.getenv(
        "DEV_SECRET_KEY", "You can't see California without Marlon Widgeto's eyes"
    )
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "Thanos did nothing wrong")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "I'm Ron Burgundy?")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
