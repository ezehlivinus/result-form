# Generated by Django 3.0.1 on 2020-03-11 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0018_auto_20200310_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='classaverage',
            name='number_in_class',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
