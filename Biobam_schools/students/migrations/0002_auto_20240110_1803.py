# Generated by Django 3.2.3 on 2024-01-10 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='ac_session',
        ),
        migrations.RemoveField(
            model_name='student',
            name='term',
        ),
        migrations.AddField(
            model_name='student',
            name='year_of_addmission',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]