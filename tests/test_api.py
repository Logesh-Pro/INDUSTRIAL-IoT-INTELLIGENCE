from backend.api.app import app


required_routes = {
    "/",
    "/api/health",
    "/api/health/database",
    "/api/system",
    "/api/system/info",
    "/api/latest",
    "/api/summary",
    "/api/devices",
    "/api/devices/<device_id>",
    "/api/history",
    "/api/alarms",
    "/api/trends"
}


def test_routes():

    routes = {
        rule.rule
        for rule in app.url_map.iter_rules()
    }

    missing = required_routes - routes

    if missing:

        raise AssertionError(
            f"Missing routes: {sorted(missing)}"
        )

    print("API ROUTES: OK")
    print(
        f"Required routes: {len(required_routes)}"
    )
    print(
        f"Registered routes: {len(routes)}"
    )


if __name__ == "__main__":
    test_routes()
