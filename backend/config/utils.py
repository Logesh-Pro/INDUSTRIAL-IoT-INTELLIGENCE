from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc)


def iso_now():
    return utc_now().isoformat()


def calculate_age(timestamp):
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return max(
        0,
        (utc_now() - timestamp).total_seconds()
    )
