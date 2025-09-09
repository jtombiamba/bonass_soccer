# workflow_manager/workflow_parser.py
import yaml
from datetime import datetime, timedelta
from celery.schedules import crontab


def parse_schedule(schedule_str):
    """Convert cron syntax to Celery crontab schedule"""
    if schedule_str.startswith('every '):
        return parse_interval(schedule_str)

    parts = schedule_str.split()
    if len(parts) != 5:
        raise ValueError("Invalid cron format")

    return crontab(
        minute=parts[0],
        hour=parts[1],
        day_of_month=parts[2],
        month_of_year=parts[3],
        day_of_week=parts[4]
    )


def parse_interval(interval_str):
    """Parse interval strings like 'every 5 minutes'"""
    parts = interval_str.split()
    if len(parts) != 3 or parts[0] != 'every':
        raise ValueError("Invalid interval format")

    number = int(parts[1])
    unit = parts[2].rstrip('s')

    return timedelta(**{f"{unit}s": number})