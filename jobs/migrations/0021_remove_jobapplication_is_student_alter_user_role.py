# Generated by Django 4.2.11 on 2024-07-18 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0020_rename_companytype_employmenttype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplication',
            name='is_student',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Ứng viên'), (1, 'Nhà tuyển dụng')], null=True),
        ),
    ]
