# Generated by Django 3.0.1 on 2020-02-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0002_auto_20200224_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=6),
        ),
    ]
