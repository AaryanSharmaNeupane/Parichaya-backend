# Generated by Django 4.0.1 on 2022-02-15 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share_link', '0016_alter_sharelink_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sharelink',
            old_name='key',
            new_name='encryption_key_hash',
        ),
    ]