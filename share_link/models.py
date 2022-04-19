from ctypes.wintypes import SHORT
import os
import uuid
import shortuuid
from shortuuid.django_fields import ShortUUIDField
from django.conf import settings
from django.db import models
from django.utils import timezone


def now_plus_7():
    return timezone.now()+timezone.timedelta(days=7)


class ShareLink(models.Model):
    """Share link"""
    id = ShortUUIDField(length=16,
                        # alphabet="abcdefg1234",
                        # prefix="id_",
                        max_length=40,
                        primary_key=True, editable=False,)
    encryption_key_hash = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(
        default=now_plus_7,)

    @property
    def has_expired(self):
        return self.expiry_date < timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)


class SharedDocument(models.Model):
    """Shared Identity Document"""

    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE)

    share_link = models.ForeignKey(
        ShareLink, on_delete=models.CASCADE, related_name='documents', )
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


def document_image_file_path(instance, filename):
    """Generate file path for new document image"""
    ext = filename.split('.')[-1]
    filename = f'{shortuuid.uuid()}.{ext}'
    return os.path.join(f'uploads/shared_document/{instance.document.share_link.id}', filename)


class SharedDocumentImage(models.Model):
    """Image of document object"""
    document = models.ForeignKey(
        SharedDocument, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=document_image_file_path,)

    def __str__(self):
        return f'{self.document.title}-{self.id}'

    @property
    def filename(self):
        return os.path.basename(self.image.name)
