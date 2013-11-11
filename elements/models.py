# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField


class DataSource(models.Model):
    url = models.URLField(null=False, help_text="""
            Provide a valid URL otherwise the database population will fail.
            The URL should return a csv file.
            This operation take some time to complete.""")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name = _("DataSource")
        verbose_name_plural = _("DataSources")

    def __unicode__(self):
        return self.url


# populate db.
def populate_db(sender, **kwargs):
    call_command('populate', kwargs['instance'].url)
post_save.connect(populate_db, sender=DataSource)


class Imagen(models.Model):
    title = models.CharField(max_length=50)
    image = ImageField(upload_to='images', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name = _("Imagen")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        return slugify("%s-%s" % (self.title, self.created_at))


class Item(models.Model):
    """
    """
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    imagen = models.ForeignKey(Imagen, null=True)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        return super(Item, self).save(*args, **kwargs)


