# Generated by Django 3.0.4 on 2020-04-12 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0004_auto_20200412_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_ill',
            field=models.BooleanField(default=False),
        ),
    ]
