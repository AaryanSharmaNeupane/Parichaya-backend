# Generated by Django 4.0.1 on 2022-02-15 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_link', '0015_sharelink_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharelink',
            name='key',
            field=models.CharField(max_length=255),
        ),
    ]