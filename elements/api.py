# -*- coding: utf-8 -*-

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource, ALL

from elements.models import DataSource, Item, Imagen

class DataSourceResource(ModelResource):
    class Meta:
        queryset = DataSource.objects.all()
        resource_name = 'datasource'
        exclude = ['created_at']
        authorization = Authorization()


class ImagenResource(ModelResource):
    class Meta:
        queryset = Imagen.objects.all()
        resource_name = 'imagen'
        exclude = ['created_at']
        authorization = Authorization()
        cache = SimpleCache(timeout=60)


class ItemResource(ModelResource):

    imagen = fields.ForeignKey(ImagenResource, 'imagen', full=True, null=True)

    class Meta:
        #allowed_methods = ['get']
        queryset = Item.objects.all()
        resource_name = 'item'
        filtering = {
                'title': ALL,
                'description': ALL,
                }
        exclude = ['created_at']

        # TODO:
        # Use authentication/authorization classes available in Tastypie
        authorization = Authorization()

        # These caches store at the object level, reducing access time on the database.
        # TODO:
        # use of a caching proxy, like Varnish, as it shines under this kind of usage.
        cache = SimpleCache(timeout=60)

