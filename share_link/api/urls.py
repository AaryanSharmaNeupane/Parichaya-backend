from xml.etree.ElementInclude import include
from django.urls import path, re_path

from share_link import views
from share_link.api import views as api_views

app_name = 'share_link'


urlpatterns = [
    path('', api_views.CreateShareLink.as_view(), name='create_share_link'),


    path('<str:share_link_id>/<str:encryption_key>/',
         api_views.ShareLinkDetail.as_view(), name='share_link_details'),

    path('<str:share_link_id>/<str:encryption_key>/add-document/',
         api_views.AddSharedDocument.as_view(), name='add_shared_document'),

    path('image/<int:shared_document_image_id>/<str:encryption_key>/',
         api_views.view_shared_document_image, name='view_shared_document_image'),

    path('image/<int:shared_document_image_id>/<str:encryption_key>/download/',
         api_views.download_shared_document_image, name='download_shared_document_image'),


    path('document/<int:shared_document_id>/images/<str:encryption_key>/download/',
         api_views.download_document_wise_images, name='download_document_wise_images'),
    path('<str:share_link_id>/images/<str:encryption_key>/download/',
         api_views.download_all_share_link_images, name='download_all_share_link_images'),


    # WORKING----------
    #     path('document-image/<uuid:document_image_id>/<str:encryption_key>/', views.view_shared_document_image,
    #          name='view_shared_document_image'),

    #     #     path('<uuid:share_link_id>/', api_views.ShareLinkDetail.as_view(),
    #     path('download_image/<int:document_image_id>/<str:encryption_key>/', views.download_shared_document_image,
    #          name='view_shared_document_image'),
    #     path('<uuid:share_link_id>/', api_views.ShareLinkDetail.as_view(),
    #          name='share_link_details'),


    #     path('<uuid:share_link_id>/documents/',
    #          api_views.SharedDocumentList.as_view(), name='shared_document_lists'),

    #     path('<uuid:share_link_id>/documents/add/<str:encryption_key>/',
    #          api_views.SharedDocumentAdd.as_view(), name='add_shared_document'),
    #     #     re_path(r'^(?P<share_link_id>{})/documents/add/(?P<base64string>{})'.format(
    #     #         uuid_pattern, base64_pattern), views.SharedDocumentAdd.as_view(), name='add_shared_document'),
    #     #   views.SharedDocumentAdd.as_view(), name='add_shared_document'),
    #     #     path('<uuid:share_link_id>/documents/',
    #     #          include('document.urls')),
    #     path('<uuid:share_link_id>/documents/<int:shared_document_id>/',
    #          api_views.SharedDocumentDetail.as_view(), name='shared_document_details'),

    #     path('<uuid:share_link_id>/documents/<int:shared_document_id>/images/', api_views.SharedDocumentImageList.as_view(),
    #          name='shared_document_image_lists'),
    #     path('<uuid:share_link_id>/documents/<int:shared_document_id>/images/<int:shared_document_image_id>/', api_views.SharedDocumentImageDetail.as_view(),
    #          name='shared_document_image_details'),



]
