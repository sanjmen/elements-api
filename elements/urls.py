# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from elements.api import DataSourceResource, ItemResource, ImagenResource

v1_api = Api(api_name='v1')
v1_api.register(ItemResource())
v1_api.register(ImagenResource())
v1_api.register(DataSourceResource())



item_resource = ItemResource()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

