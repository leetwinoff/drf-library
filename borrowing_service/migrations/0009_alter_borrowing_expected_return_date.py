# Generated by Django 4.2.1 on 2023-06-09 02:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing_service", "0008_alter_borrowing_expected_return_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="expected_return_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 6, 16, 2, 59, 9, 667528, tzinfo=datetime.timezone.utc
                ),
                editable=False,
            ),
        ),
    ]