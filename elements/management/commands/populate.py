# -*- coding: UTF-8 -*-

import os
import csv
from StringIO import StringIO
from tempfile import NamedTemporaryFile

from django.core.management.base import BaseCommand
from django.core.files import File
from django.template.defaultfilters import slugify

import requests

from elements.models import Item, Imagen

class Command(BaseCommand):
    help = """Fetch the resource, get CSV feed,
              parse && add the resulting items to our db.
              example url:
              https://docs.google.com/spreadsheet/pub?key=0Am6xRuJpTz1wdGpHWk1FZHNtZ0RyUGswdVp1T1BFeUE&single=true&gid=0&output=csv
           """
    args = "<source_url>"

    def handle(self, *args, **options):
        if not len(args):
            print "You must provide the source url as parameter"
            exit(0)

        source_url = args[0]
        r = requests.get(source_url)

        if r.status_code > 400:
            print "status_code: %s. You must provide a valid URL" % r.status_code
            return

        if r.headers['content-type'] != 'text/csv':
            print "the source url should return a csv file"
            return

        if r.status_code is 200:

            reader = csv.DictReader(StringIO(r.text), delimiter=',')
            for dataitem in reader:

                # get image and save
                image_url = dataitem['image']

                if image_url is not '':
                    try:
                        splitted_name = os.path.basename(image_url).split('.')
                        ext = splitted_name[-1].lower()
                        slug = slugify(".".join(splitted_name[:-1]))
                        if len(slug) > 25:
                            slug = slug[:25]
                        name = "%s.%s" % (slug, ext)
                        if not (ext in ["jpg", "jpeg"]):
                            print "File not JPG", name
                            continue

                    except Exception, e:
                        print e

                    image_req = requests.get(image_url)
                    img_file = NamedTemporaryFile()
                    img_file.write(image_req.content)

                    img = Imagen()
                    img.title = slug
                    img.image.save(name, File(img_file), save=True)
                    img.save()

                    img_file.close()
                    print "image saved : %s" % img.title
                else:
                    img = None

                # get or create new item with title, description and imagen attributes
                title = dataitem['title']
                description = dataitem['description']

                item, created = Item.objects.get_or_create(title=title, description=description, imagen=img)

                if created:
                    print 'created: %s' % item.title

        print 'done'
