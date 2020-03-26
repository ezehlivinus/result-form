# Generated by Django 3.0.1 on 2020-03-06 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0016_result_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='class_average',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='result',
            name='pupil_average',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='result',
            name='total_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(choices=[('english/verbal', 'English/Verbal'), ('spelling', 'Spelling'), ('Basic Science', 'Basic Science'), ('Physics', 'Physics')], max_length=100, unique=True, verbose_name='Title'),
        ),
    ]
