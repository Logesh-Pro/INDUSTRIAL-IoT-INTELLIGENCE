from backend.config.settings import settings
from backend.database.influx import InfluxDatabase


class DatabaseHealth:

    def __init__(self):
        self.db = InfluxDatabase()

    def check(self):

        try:

            health = self.db.client.health()

            return {
                "status": "healthy",
                "database": "InfluxDB",
                "message": health.message,
                "version": health.version,
                "url": settings.INFLUX_URL,
                "organization": settings.INFLUX_ORG,
                "bucket": settings.INFLUX_BUCKET
            }

        except Exception as exc:

            return {
                "status": "unhealthy",
                "database": "InfluxDB",
                "message": str(exc),
                "url": settings.INFLUX_URL,
                "organization": settings.INFLUX_ORG,
                "bucket": settings.INFLUX_BUCKET
            }

    def close(self):
        self.db.close()
