# Generated by Django 4.2.3 on 2023-07-26 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_access', '0002_alter_dataset_columns'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='columns',
            field=models.TextField(blank=True, null=True),
        ),
    ]