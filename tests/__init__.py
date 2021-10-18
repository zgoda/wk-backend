import time


def days_from_now_millis(days: int) -> int:
    return int((days * 24 * 60 * 60 + time.time()) * 1000)
