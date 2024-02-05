# Generated by Django 5.0.1 on 2024-01-29 09:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("WorkplaceApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StdntLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stuid", models.CharField(default=None, max_length=200)),
                ("title", models.CharField(max_length=200)),
                ("date", models.DateField()),
                ("summary", models.TextField()),
                ("description", models.TextField()),
                ("lect_comment", models.TextField(default=None)),
            ],
        ),
        migrations.DeleteModel(
            name="StudentLog",
        ),
    ]
