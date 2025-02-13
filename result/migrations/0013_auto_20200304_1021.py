# Generated by Django 3.0.1 on 2020-03-04 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0012_auto_20200304_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='is_for_junior',
            new_name='is_offered_by_junior',
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(choices=[('english/verbal', 'English/Verbal'), ('spelling', 'Spelling'), ('Basic Science', 'Basic Science')], max_length=100, unique=True, verbose_name='Title'),
        ),
    ]
