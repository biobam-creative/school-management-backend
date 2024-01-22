# Generated by Django 3.2.3 on 2024-01-10 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_tools', '0003_auto_20240110_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='term',
            name='school_fee',
        ),
        migrations.CreateModel(
            name='SchoolFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=10000)),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_tools.studentclass')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_tools.term')),
            ],
        ),
    ]