# Generated by Django 4.2.11 on 2024-10-03 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0039_remove_jobseeker_applied_job_invoice_product_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker',
            name='applied_job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobseekers', to='jobs.job'),
        ),
    ]
