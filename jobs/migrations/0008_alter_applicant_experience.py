# Generated by Django 4.2.11 on 2024-04-17 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_alter_jobapplication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]
