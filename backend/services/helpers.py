from datetime import datetime, timezone


def validate_hours(value, default=24, maximum=168):
    try:
        hours = int(value)

        if hours < 1:
            return default

        if hours > maximum:
            return maximum

        return hours

    except (TypeError, ValueError):
        return default


def is_online(last_seen, timeout=10):
    if not last_seen:
        return False

    if isinstance(last_seen, str):
        last_seen = datetime.fromisoformat(last_seen)

    if last_seen.tzinfo is None:
        last_seen = last_seen.replace(
            tzinfo=timezone.utc
        )

    age = (
        datetime.now(timezone.utc) - last_seen
    ).total_seconds()

    return age <= timeout
