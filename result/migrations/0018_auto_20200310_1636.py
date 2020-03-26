# Generated by Django 3.0.1 on 2020-03-10 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0017_auto_20200306_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='class_average',
        ),
        migrations.RemoveField(
            model_name='result',
            name='pupil_average',
        ),
        migrations.RemoveField(
            model_name='result',
            name='total_score',
        ),
        migrations.CreateModel(
            name='TotalScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.IntegerField(default=0)),
                ('average_score', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.Grade')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.Session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.Student')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.Term')),
            ],
        ),
        migrations.CreateModel(
            name='ClassAverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_average', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.TotalScore')),
            ],
        ),
    ]
