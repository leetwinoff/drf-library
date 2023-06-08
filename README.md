# Library Service Project

This is a project to develop an online management system for book borrowings in a library. The goal is to optimize the work of library administrators and create a more user-friendly service.
- Implement a web-based system for book borrowings.
- Manage the inventory of books.
- Handle book borrowing transactions.
- Manage customer information.
- Display notifications for borrowings/returns and overdue.
- Handle payments for book borrowings.
- drf-spectacular documentation


## Installation

Clone link from GutHub [drf-library](https://github.com/leetwinoff/drf-library.git)



```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Notification service installation

Project supports sending notification via telegram for various occasions. Skip telegram part if you don't need this.

### Create telegram bot

- Proceed to https://telegram.me/BotFather or search for BotFather in your telegram app
- Click Start
- Type /newbot and follow short instructions
- Receive the bot token - store it safely!!!

### Create telegram group

- Create telegram group where notifications received
- Add telegram bot that you've just created to group
- Type something in newly created group
- Navigate to https://api.telegram.org/botXXX:YYYYY/getUpdates (replace the XXX: YYYYY with your BOT HTTP API Token you just got from the Telegram BotFather)
- Look for the chat object - store it safely!!!

## Payment service installation

Project supports Stripe Payment sessions

- Initialize your Stripe Payment account (you can select for example USA as a country)
- Navigate to dashboard and copy test data to your project(add STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY to your .env)


#

Create .env file in root directory and store there your secret information like shown in .env.sample

### Make migrations 

```bash
python manage.py migrate
python manage.py runserver
```

#

If you want to receive daily telegram messages about borrowings to be expired tomorrow, run command below in separate terminal

```bash
celery -A drf_library worker -l INFO
```
```bash
celery -A drf_library beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Testing with admin

Email: admin@admin.com

Password: admin1234

#### You can create your own admin user or register a new user to test non-admin functionality

