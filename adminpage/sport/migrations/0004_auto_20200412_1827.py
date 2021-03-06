# Generated by Django 3.0.4 on 2020-04-12 15:27

from django.db import migrations, models
import functools
import sport.models.semester


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0003_auto_20200405_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='choice_deadline',
            field=models.DateTimeField(default=functools.partial(sport.models.semester.now_offset, *(1,), **{})),
        ),
        migrations.AddField(
            model_name='semester',
            name='end',
            field=models.DateTimeField(default=functools.partial(sport.models.semester.now_offset, *(2,), **{})),
        ),
        migrations.AddField(
            model_name='semester',
            name='start',
            field=models.DateTimeField(default=functools.partial(sport.models.semester.now_offset, *(0,), **{})),
        ),
    ]
