# Generated by Django 4.0.1 on 2022-02-13 06:40

from django.db import migrations, models
import share_link.models


class Migration(migrations.Migration):

    dependencies = [
        ('share_link', '0010_alter_sharelink_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareddocumentimage',
            name='image',
            field=models.FileField(upload_to=share_link.models.document_image_file_path),
        ),
    ]