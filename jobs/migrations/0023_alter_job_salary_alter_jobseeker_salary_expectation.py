# Generated by Django 4.2.11 on 2024-07-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0022_alter_jobapplication_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='salary_expectation',
            field=models.CharField(max_length=255),
        ),
    ]
