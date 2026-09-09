from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from backend.config.settings import settings


class InfluxDatabase:

    def __init__(self):
        self.client = InfluxDBClient(
            url=settings.INFLUX_URL,
            token=settings.INFLUX_TOKEN,
            org=settings.INFLUX_ORG
        )

        self.write_api = self.client.write_api(
            write_options=SYNCHRONOUS
        )

        self.query_api = self.client.query_api()

    def write(self, point):
        self.write_api.write(
            bucket=settings.INFLUX_BUCKET,
            org=settings.INFLUX_ORG,
            record=point
        )

    def query(self, query):
        return self.query_api.query(
            query,
            org=settings.INFLUX_ORG
        )

    def close(self):
        self.client.close()
