from dataclasses import field
from pyexpat import model
from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import ShareLink, SharedDocument, SharedDocumentImage


class SharedDocumentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedDocumentImage
        fields = ('id', )
        read_only_fields = ('id',)


class SharedDocumentSerializer(serializers.ModelSerializer):
    images = SharedDocumentImageSerializer(many=True, read_only=True)

    class Meta:
        model = SharedDocument
        fields = ('id', 'title', 'images')
        read_only_fields = ('id', 'images')

    def create(self, validated_data):
        data = validated_data.copy()
        shared_document = SharedDocument.objects.create(**validated_data)

        # print(self.context.get('request').FILES['images'])

        if('images' in self.context.get('request').data):
            shared_images_data = self.context.get('request').data.pop('images')

            for shared_image_data in shared_images_data:
                SharedDocumentImage.objects.create(
                    document=shared_document, image=shared_image_data)

        return shared_document


# class SenderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ('id', 'name', 'mobile')


class ShareLinkSerializer(serializers.ModelSerializer):
    # sender = SenderSerializer(read_only=True)
    documents = SharedDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ShareLink
        fields = ('id', 'title', 'created_on', 'expiry_date',  'documents')
        read_only_fields = ('id', 'documents',)

    # def create(self, validated_data):
    #     shared_documents_data = validated_data.pop('documents')
    #     share_link = ShareLink.objects.create(**validated_data)
    #     for shared_document_data in shared_documents_data:
    #         SharedDocument.objects.create(
    #             share_link=share_link, **shared_document_data)
    #     return share_link


class xSharedDocumentSerializer(serializers.ModelSerializer):
    images = SharedDocumentImageSerializer(many=True, read_only=True)

    class Meta:
        model = SharedDocument
        fields = ('id', 'title', 'images')
        read_only_fields = ('id', 'images',)
