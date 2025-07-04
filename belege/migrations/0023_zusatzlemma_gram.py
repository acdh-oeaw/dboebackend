# Generated by Django 5.2.1 on 2025-07-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("belege", "0022_alter_zusatzlemma_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="zusatzlemma",
            name="gram",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Subst", "Subst"),
                    ("Interj", "Interj"),
                    ("Verb", "Verb"),
                    ("Adj", "Adj"),
                ],
                max_length=20,
                null=True,
                verbose_name="Grammatik",
            ),
        ),
    ]
