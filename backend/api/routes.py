from flask import Blueprint, jsonify, request

from backend.services.device_service import DeviceService
from backend.services.event_service import EventService
from backend.services.system_service import SystemService
from backend.services.device_event_service import DeviceEventService
from backend.database.influx import InfluxDatabase
from backend.api.health_routes import register_database_health_route

api = Blueprint("api", __name__)

device_service = DeviceService()
event_service = EventService()
system_service = SystemService()
device_event_service = DeviceEventService()
db = InfluxDatabase()

register_database_health_route(api)


@api.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "database": "connected",
        "mqtt": "managed-by-telemetry-processor"
    })


@api.route("/system")
def system():
    return jsonify(system_service.get_status())


@api.route("/latest")
def latest():

    query = '''
    from(bucket: "telemetry")
      |> range(start: -5m)
      |> filter(fn: (r) => r["_measurement"] == "environment")
      |> group(columns: ["device_id", "_field"])
      |> last()
    '''

    tables = db.query(query)

    data = {}

    for table in tables:
        for record in table.records:
            data[record.get_field()] = record.get_value()

    return jsonify(data)


@api.route("/summary")
def summary():

    devices = device_service.get_devices()

    online = 0
    offline = 0
    total_people = 0

    for device in devices:

        if device.get("status") == "online":
            online += 1

        elif device.get("status") == "offline":
            offline += 1

        total_people += int(
            device.get("people", 0)
        )

    return jsonify({
        "total_devices": len(devices),
        "online_devices": online,
        "offline_devices": offline,
        "total_people": total_people
    })


@api.route("/device-events")
def device_events():
    try:
        hours = int(request.args.get("hours", 24))

        if hours < 1 or hours > 168:
            return jsonify({
                "status": "error",
                "message": "hours must be between 1 and 168"
            }), 400

        data = device_event_service.get_events(hours)

        return jsonify({
            "count": len(data),
            "hours": hours,
            "events": data
        })

    except ValueError:
        return jsonify({
            "status": "error",
            "message": "hours must be an integer"
        }), 400
    except Exception as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        }), 500

@api.route("/devices")
def devices():

    device_list = device_service.get_devices()

    return jsonify({
        "count": len(device_list),
        "devices": device_list
    })


@api.route("/devices/<device_id>")
def device(device_id):

    result = device_service.get_device(device_id)

    if result is None:

        return jsonify({
            "status": "error",
            "message": "Device not found",
            "device_id": device_id
        }), 404

    return jsonify(result)


@api.route("/history")
def history():

    try:

        hours = int(
            request.args.get("hours", 24)
        )

        if hours < 1 or hours > 168:

            return jsonify({
                "status": "error",
                "message": "hours must be between 1 and 168"
            }), 400

        data = event_service.get_history(hours)

        return jsonify({
            "count": len(data),
            "hours": hours,
            "data": data
        })

    except ValueError:

        return jsonify({
            "status": "error",
            "message": "hours must be an integer"
        }), 400


@api.route("/alarms/active")
def active_alarms():
    try:
        return jsonify(event_service.get_active_alarms())
    except Exception as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        }), 500
@api.route("/alarms")
def alarms():

    try:

        hours = int(
            request.args.get("hours", 24)
        )

        if hours < 1 or hours > 168:

            return jsonify({
                "status": "error",
                "message": "hours must be between 1 and 168"
            }), 400

        data = event_service.get_alarms(hours)

        return jsonify({
            "count": len(data),
            "hours": hours,
            "alarms": data
        })

    except ValueError:

        return jsonify({
            "status": "error",
            "message": "hours must be an integer"
        }), 400


@api.route("/trends")
def trends():

    query = '''
    from(bucket: "telemetry")
      |> range(start: -1h)
      |> filter(fn: (r) => r["_measurement"] == "environment")
      |> filter(fn: (r) =>
          r["_field"] == "temperature" or
          r["_field"] == "humidity" or
          r["_field"] == "people"
      )
      |> aggregateWindow(
          every: 1m,
          fn: mean,
          createEmpty: false
      )
      |> sort(columns: ["_time"])
    '''

    tables = db.query(query)

    data = []

    for table in tables:

        for record in table.records:

            data.append({
                "timestamp": record.get_time().isoformat(),
                "device_id": record.values.get("device_id"),
                "field": record.get_field(),
                "value": record.get_value()
            })

    return jsonify({
        "count": len(data),
        "data": data
    })




