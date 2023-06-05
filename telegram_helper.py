import os
from dotenv import load_dotenv
import requests


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
