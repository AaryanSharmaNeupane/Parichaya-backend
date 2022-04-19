# from django.core.servers.basehttp import FileWrapper
from django.http import FileResponse
from wsgiref.util import FileWrapper
import mimetypes
from django.http import HttpResponse
from encrypted_files.base import EncryptedFile
from ..models import SharedDocumentImage
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


from share_link.models import ShareLink, SharedDocument, SharedDocumentImage
from share_link.api.serializers import ShareLinkSerializer, SharedDocumentSerializer, SharedDocumentImageSerializer


# @api_view(['GET'])
# def urls_overview(request):
#     data = {
#         'Create': '/create',
#         'List': '/',
#         'Detail View': '/<str:pk>/',
#     }
#     return Response(data=data, status=status.HTTP_200_OK)


class ShareLinkList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        share_links = ShareLink.objects.filter(sender=request.user)
        serializer = ShareLinkSerializer(share_links, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ShareLinkSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareLinkDetail(APIView):
    # def get_object(self, pk):
    #     try:
    #         return ShareLink.objects.get(pk=pk)
    #     except (ShareLink.DoesNotExist, ValidationError):
    #         raise Http404
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, share_link_id, format=None):
        share_link = get_object_or_404(ShareLink, pk=share_link_id)
        serializer = ShareLinkSerializer(share_link)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, share_link_id, format=None):
        share_link = get_object_or_404(ShareLink, pk=share_link_id)
        serializer = ShareLinkSerializer(share_link, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, share_link_id, format=None):
        share_link = get_object_or_404(ShareLink, pk=share_link_id)
        share_link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SharedDocumentList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, share_link_id, format=None):
        share_link = get_object_or_404(ShareLink, pk=share_link_id)
        shared_documents = share_link.documents.all()
        serializer = SharedDocumentSerializer(shared_documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SharedDocumentAdd(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, share_link_id, encryption_key, format=None):
        share_link = get_object_or_404(ShareLink, pk=share_link_id)
        # key = os.urandom(16)
        # if 'encryption_key' not in request.data:
        #     return Response({'detail': 'encryption_key is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # request_copy = request.data.copy()
        # key = request.data.get('encryption_key')
        # encryption_key = 'asimnepal'
        key_string = hashlib.sha256(encryption_key.encode())
        byte_key = key_string.digest()
        # key = b',Ca8\xcc}\x1b\x8a\x8f_\xe6\xac\xa7\x93\xa6K'
        # key = os.urandom(16)
        # key = bytes(encryption_key, 'utf-8')
        request.upload_handlers = [
            EncryptedFileUploadHandler(request=request, key=byte_key),
            MemoryFileUploadHandler(request=request),
            TemporaryFileUploadHandler(request=request)
        ]
        print(request.upload_handlers)
        serializer = SharedDocumentSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(share_link=share_link)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SharedDocumentDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, share_link_id, shared_document_id, format=None):
        shared_document = get_object_or_404(
            SharedDocument, pk=shared_document_id, share_link__id=share_link_id)
        serializer = SharedDocumentSerializer(shared_document)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, share_link_id, shared_document_id, format=None):
        shared_document = get_object_or_404(
            SharedDocument, pk=shared_document_id, share_link__id=share_link_id)
        serializer = SharedDocumentSerializer(
            shared_document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, share_link_id, shared_document_id, format=None):
        shared_document = get_object_or_404(
            SharedDocument, pk=shared_document_id, share_link__id=share_link_id)
        shared_document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SharedDocumentImageList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, share_link_id, shared_document_id, format=None):
        shared_document = get_object_or_404(
            SharedDocument, pk=shared_document_id, share_link__id=share_link_id)
        shared_document_images = shared_document.images.all()
        serializer = SharedDocumentImageSerializer(
            shared_document_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,  share_link_id, shared_document_id, format=None):
        shared_document = get_object_or_404(
            SharedDocument, pk=shared_document_id, share_link__id=share_link_id)

        serializer = SharedDocumentImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(document=shared_document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SharedDocumentImageDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, share_link_id, shared_document_id, shared_document_image_id, format=None):
        shared_document_image = get_object_or_404(
            SharedDocumentImage, pk=shared_document_image_id, document__id=shared_document_id, document__share_link__id=share_link_id)
        serializer = SharedDocumentImageSerializer(shared_document_image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, share_link_id, shared_document_id, shared_document_image_id, format=None):
        shared_document_image = get_object_or_404(
            SharedDocumentImage, pk=shared_document_image_id, document__id=shared_document_id, document__share_link__id=share_link_id)
        serializer = SharedDocumentImageSerializer(
            shared_document_image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, share_link_id, shared_document_id, shared_document_image_id, format=None):
        shared_document_image = get_object_or_404(
            SharedDocument, pk=shared_document_image_id, document__id=shared_document_id, document__share_link__id=share_link_id)
        shared_document_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def share_link_details_api(request, pk):
#     try:
#         share_link = ShareLink.objects.get(pk=pk)
#     except ShareLink.DoesNotExist():
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = ShareLinkSerializer(share_link)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['PUT'])
# def share_link_update_api(request, pk):
#     try:
#         share_link = ShareLink.objects.get(pk=pk)
#     except ShareLink.DoesNotExist():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = ShareLinkSerializer(share_link, data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data['success'] = 'updated successfully'
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE', ])
# def share_link_delete_api(request, pk):
#     try:
#         share_link = ShareLink.objects.get(pk=pk)
#     except ShareLink.DoesNotExist():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'DELETE':
#         operation = share_link.delete()
#         data = {}
#         if operation:
#             data['success'] = 'delete successful'
#             return Response(data=data, status=status.HTTP_200_OK)
#         else:
#             data['failure'] = 'delete failed'
#             return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
