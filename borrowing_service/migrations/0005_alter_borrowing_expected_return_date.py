# Generated by Django 4.2.1 on 2023-06-07 02:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing_service", "0004_alter_borrowing_expected_return_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="expected_return_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 6, 14, 2, 4, 5, 650664, tzinfo=datetime.timezone.utc
                ),
                editable=False,
            ),
        ),
    ]