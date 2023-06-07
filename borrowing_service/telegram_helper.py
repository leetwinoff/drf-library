from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests
from django.db.models import Q

from borrowing_service.models import Borrowing

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_borrowing_notification(borrowing: Borrowing) -> None:
    text = (
        f"Borrowing id: {borrowing.id}\n"
        f"Borrowing date: {borrowing.borrow}\n"
        f"Borrowing expected return date: "
        f"{borrowing.expected_return_date}\n"
        f"Book: {borrowing.book_id}\n"
        f"Customer: {borrowing.user_id}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=params)


def return_borrowing_notification(borrowing: Borrowing) -> None:
    text = (
        f"Customer: {borrowing.user_id}\n"
        f"Successfully returned\n"
        f"Borrowing id: {borrowing.id}\n"
        f"Expected return date: {borrowing.expected_return_date}\n"
        f"Actual return date {borrowing.actual_return_date}\n"
        f"Book: {borrowing.book_id}\n"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=params)


def send_overdue_notification() -> None:
    tomorrow = datetime.today() + timedelta(1)
    check_borrowing = Borrowing.objects.filter(
        Q(actual_return_date__isnull=True) & Q(expected_return_date=tomorrow)
    )
    if check_borrowing:
        for borrowing in check_borrowing:
            text = (
                f"Customer: {borrowing.user_id}\n"
                f"Borrowed Book: {borrowing.book_id} ends tomorrow\n"
                f"Expected return date: {borrowing.expected_return_date}\n"
            )

            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
            requests.post(url, json=params)
    else:
        text = "No borrowings overdue today!"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
        requests.post(url, json=params)
