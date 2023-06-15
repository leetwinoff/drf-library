from borrowings.telegram_helper import send_overdue_notification
from drf_library.celery import app


@app.task
def send_notification():
    return send_overdue_notification()
