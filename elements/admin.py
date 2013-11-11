# -*- coding: UTF-8 -*-
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from elements.models import DataSource, Item, Imagen

class ImagenAdmin(AdminImageMixin, admin.ModelAdmin):
        pass

admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Item)
admin.site.register(DataSource)
