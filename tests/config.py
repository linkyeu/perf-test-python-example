import logging
from dataclasses import dataclass

from influxdb_client import InfluxDBClient, WriteOptions


class LogConfig:
    logger = logging.getLogger('demo_logger')
    logger.setLevel('DEBUG')
    file = logging.FileHandler(filename='test_logs.log')
    file.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(file)
    logger.propagate = False


class Config:
    conf_name = "DenysConfig"
    pacing_sec = 0.1
    api_host = 'http://localhost:8000'
    influx_bucket = 'mybucket'
    influx_org = 'myorg'
    influx_client = InfluxDBClient(
        url="http://localhost:8086",
        token='myadmintoken',
        org=influx_org,
    )
    influxdb = influx_client.write_api(
        write_options=WriteOptions(
            batch_size=10,
            flush_interval=10_000,
            jitter_interval=2_000,
            retry_interval=5_000,
        )
    )


@dataclass
class EndpointUrls:
    BASE_URL: str = "http://localhost:8000"
    ADD: str = BASE_URL + "/addBook"
    DELETE: str = BASE_URL + "/deleteBook"
    GET_BOOKS: str = BASE_URL + "/books"
    VIEW_BY_ID: str = BASE_URL + "/viewBookByID"


endpoint = EndpointUrls()
logger = LogConfig().logger
cfg = Config()
