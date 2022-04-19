from django.contrib import admin
from share_link import models
# Register your models here.

admin.site.register(models.ShareLink)
admin.site.register(models.SharedDocument)
admin.site.register(models.SharedDocumentImage)
