# Generated by Django 3.0.1 on 2020-03-04 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0013_auto_20200304_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='teacher',
            field=models.ForeignKey(default=1, help_text='This is the class teacher for this grade', on_delete=django.db.models.deletion.CASCADE, to='result.Teacher', verbose_name='Grade Teacher'),
            preserve_default=False,
        ),
    ]
