from flask import jsonify

from backend.database.influx import InfluxDatabase


def register_database_health_route(api):
    @api.route("/health/database")
    def database_health():
        db = None

        try:
            db = InfluxDatabase()

            # Execute a lightweight query to verify that
            # the API can actually communicate with InfluxDB.
            query = '''
            from(bucket: "telemetry")
              |> range(start: -1m)
              |> limit(n: 1)
            '''

            db.query(query)

            return jsonify({
                "status": "connected",
                "database": "InfluxDB",
                "url": "configured",
                "message": "Database connection is healthy"
            })

        except Exception as exc:
            return jsonify({
                "status": "disconnected",
                "database": "InfluxDB",
                "message": str(exc)
            }), 503

        finally:
            if db is not None:
                db.close()
