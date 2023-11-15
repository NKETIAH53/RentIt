# Generated by Django 4.2.3 on 2023-11-15 09:33

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                default="+233244000000",
                max_length=20,
                region=None,
                verbose_name="Phone Number",
            ),
        ),
    ]
