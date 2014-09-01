from datetime import datetime
from io import BytesIO
from tarfile import TarInfo, TarFile

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.encoding import smart_bytes

from twobuntu.ads.models import Ad
from twobuntu.categories.models import Category
from twobuntu.images.models import Image


class MixedIO(BytesIO):
    """
    A BytesIO that accepts and encodes Unicode data.
    """

    def rewind(self):
        size = self.tell()
        self.seek(0)
        return size

    def write(self, data):
        BytesIO.write(self, smart_bytes(data))


class Command(BaseCommand):
    """
    Create a complete backup of the 2buntu website.

    This command will generate JSON files from the contents of the database and
    include all media files in a compressed .tar.xz file.
    """

    help = "Create a complete backup of the 2buntu website."

    DATABASE_MODELS = [
        'accounts.profile',
        'ads.ad',
        'articles.article',
        'articles.scheduledarticle',
        'auth.user',
        'categories.category',
        'images.image',
        'news.item',
        'shorturls.shorturl',
    ]

    IMAGE_MODELS = [
        Ad,
        Category,
        Image,
    ]

    def handle(self, *args, **kwargs):
        """
        Process the command.
        """
        tar = TarFile.open(datetime.today().strftime('2buntu-backup-%Y-%m-%d-%H-%M-%S.tar.bz2'), 'w:bz2')
        for name in self.DATABASE_MODELS:
            f = MixedIO()
            call_command('dumpdata', name, format='json', stdout=f)
            info = TarInfo('%s.json' % name.split('.')[1])
            info.size = f.rewind()
            tar.addfile(info, f)
        for model in self.IMAGE_MODELS:
            for item in model.objects.all():
                if item.image:
                    info = TarInfo(item.image.name)
                    info.size = item.image.size
                    tar.addfile(info, item.image)
        self.stdout.write("Backup completed.")
