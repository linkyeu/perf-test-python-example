import time
from functools import wraps

from locust import task, constant_pacing, HttpUser, LoadTestShape, between, tag
import random

from mock_server.main import Book
from tests.config import logger, endpoint, cfg
from locust import HttpUser, task, events
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


def proceed_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_start_time = time.time()
        transaction = func(*args, **kwargs)
        processing_time = int((time.time() - request_start_time) * 1000)

        cfg.influxdb.write(
            cfg.influx_bucket,
            cfg.influx_org,
            [{
                "measurement": f"{cfg.conf_name}_db",
                "tags": {"transaction_name": func.__name__},
                "time": time.time_ns(),
                "fields": {"response_time": processing_time},
            }],
        )

    return wrapper


class BookUser(HttpUser):
    wait_time = between(1, 5)

    @task
    @proceed_request
    def get_book(self):
        self.client.get(endpoint.GET_BOOKS)

    @task
    @proceed_request
    def add_book(self):
        self.client.post(
            url=endpoint.ADD,
            data=Book(
                id="1",
                title="Denys title",
                author="Denys",
            ).json()
        )
        time.sleep(random.normalvariate(mu=3, sigma=0.5))
        self.client.post(
            url=endpoint.ADD,
            data=Book(
                id="2",
                title="Anton title",
                author="Anton",
            ).json()
        )


    #
    # @task
    # def add_existing_book(self):
    #     self.client.get(endpoint.GET_BOOKS)
    #
    # @task
    # def add_not_existing_book(self):
    #     self.client.get(endpoint.GET_BOOKS)



#
# class BookUser(HttpUser):
#     def on_stop(self):
#         logger.debug(f"user stopped")
#
#     def add_existing_book(self) -> None:
#         with self.client.post(
#             "/cart/add",
#             headers=headers,
#             json=body,
#             catch_response=True,
#             name=transaction,
#         ) as request:
#             assertion.check_http_response(transaction, request)
#
#
# class StagesShape(LoadTestShape):
#     stages = [
#         {"duration": 20, "users": 1, "spawn_rate": 1},
#         {"duration": 40, "users": 2, "spawn_rate": 1},
#         {"duration": 60, "users": 4, "spawn_rate": 1},
#         {"duration": 80, "users": 8, "spawn_rate": 1},
#         {"duration": 100, "users": 10, "spawn_rate": 1},
#     ]
#
#     def tick(self):
#         run_time = self.get_run_time()
#         for stage in self.stages:
#             if run_time < stage["duration"]:
#                 tick_data = (stage["users"], stage["spawn_rate"])
#                 return tick_data
#         return None