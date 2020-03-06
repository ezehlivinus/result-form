# Generated by Django 3.0.1 on 2020-03-01 19:50

from django.db import migrations, models
import result.models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0005_auto_20200301_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='total',
            field=models.PositiveIntegerField(default=0, validators=[result.models.Result.validate_max]),
        ),
    ]
