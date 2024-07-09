# Generated by Django 5.0.4 on 2024-07-02 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_match_delete_matches"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="win_team",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "home_team",
                        models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE,
                            related_name="home_matches",
                            to="core.club",
                        ),
                    ),
                    (
                        "away_team",
                        models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE,
                            related_name="away_matches",
                            to="core.club",
                        ),
                    ),
                    ("draw", "Draw"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
