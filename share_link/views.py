# from django.core.servers.basehttp import FileWrapper
import zipfile
import tempfile
from django.http import FileResponse
from wsgiref.util import FileWrapper
import mimetypes
from django.http import HttpResponse
from encrypted_files.base import EncryptedFile
from .models import SharedDocumentImage
import os
import hashlib
from django.http import Http404
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.core.files.uploadhandler import MemoryFileUploadHandler, TemporaryFileUploadHandler
from encrypted_files.uploadhandler import EncryptedFileUploadHandler
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import renderers
from passlib.hash import pbkdf2_sha256

from share_link.models import ShareLink, SharedDocument, SharedDocumentImage
from share_link.api.serializers import ShareLinkSerializer, SharedDocumentSerializer, SharedDocumentImageSerializer


def view_shared_document_image(request, shared_document_image_id, encryption_key):
    shared_document_image = get_object_or_404(
        SharedDocumentImage, pk=shared_document_image_id)
    share_link = get_object_or_404(
        ShareLink, pk=shared_document_image.document.share_link.id)

    is_key_correct = pbkdf2_sha256.verify(
        encryption_key, share_link.encryption_key_hash)
    if not is_key_correct:
        return Response({'detail': 'wrong decryption key.'},
                        status=status.HTTP_400_BAD_REQUEST)
    f = SharedDocumentImage.objects.get(pk=shared_document_image_id).image
    # encryption_key = encryption_key
    key_string = hashlib.sha256(encryption_key.encode())
    byte_key = key_string.digest()
    ef = EncryptedFile(f, key=byte_key)

    response = FileResponse(ef)

    return response

    # return HttpResponse(ef.read())


def download_shared_document_image(request, pk, encryption_key,):
    f = SharedDocumentImage.objects.get(pk=pk).image
    key_string = hashlib.sha256(encryption_key.encode())
    byte_key = key_string.digest()
    # key = b',Ca8\xcc}\x1b\x8a\x8f_\xe6\xac\xa7\x93\xa6K'
    # ef = EncryptedFile(f, key=key)
    ef = EncryptedFile(f, key=byte_key)
    # img.file returns full path to the image
    wrapper = FileWrapper(ef)
    content_type = mimetypes.guess_type(
        'test.jpg')[0]  # Use mimetypes to get file type
    response = HttpResponse(wrapper, content_type=content_type)
    # response['Content-Length'] = os.path.getsize(ef)
    response['Content-Disposition'] = f"attachment; filename={'test.jpg'}"
    return response
    # response = FileResponse(ef)

    # return response

    # return HttpResponse(ef.read())


def download_all_images_by_document(request, pk, encryption_key):
    f = SharedDocumentImage.objects.get(pk=pk).image
    key_string = hashlib.sha256(encryption_key.encode())
    byte_key = key_string.digest()
    # key = b',Ca8\xcc}\x1b\x8a\x8f_\xe6\xac\xa7\x93\xa6K'
    # ef = EncryptedFile(f, key=key)
    ef = EncryptedFile(f, key=byte_key)
    # img.file returns full path to the image
    wrapper = FileWrapper(ef)
    content_type = mimetypes.guess_type(
        'test.jpg')[0]  # Use mimetypes to get file type
    response = HttpResponse(wrapper, content_type=content_type)
    # response['Content-Length'] = os.path.getsize(ef)
    response['Content-Disposition'] = f"attachment; filename={'test.jpg'}"
    return response
