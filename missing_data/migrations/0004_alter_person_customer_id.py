# Generated by Django 4.1 on 2024-04-01 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("missing_data", "0003_remove_person_id_person_age_person_customer_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="customer_id",
            field=models.IntegerField(
                auto_created=True, primary_key=True, serialize=False, unique=True
            ),
        ),
    ]
