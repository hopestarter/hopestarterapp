from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from StringIO import StringIO
from os.path import splitext

from hopebase.validators import S3URLValidator

def upload_image_to(instance, filename):
    filename_base, filename_ext = splitext(filename)
    return 'media/users/%s/%s' % (instance.user.username, filename)


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    bitcoin = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(editable=False, blank=True)
    modified = models.DateTimeField(editable=False, blank=True)
    picture = models.ImageField(upload_to=upload_image_to,
                    editable=True, null=True, blank=True, max_length=255)
    large_picture = models.ImageField(upload_to=upload_image_to,
                    editable=False, null=True, blank=True, max_length=255)
    medium_picture = models.ImageField(upload_to=upload_image_to,
                    editable=False, null=True, blank=True, max_length=255)
    small_picture = models.ImageField(upload_to=upload_image_to,
                    editable=False, null=True, blank=True, max_length=255)
    thumbnail_picture = models.ImageField(upload_to=upload_image_to,
                    editable=False, null=True, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        if self.picture:
            large_size = (800, 800)
            medium_size = (500, 500)
            small_size = (200, 200)
            thumbnail_size = (45, 45)
            # Get image name
            image_name = self.user.username
            # Resize and append
            image = Image.open(StringIO(self.picture.read()))
            image.thumbnail(large_size, Image.ANTIALIAS)
            background = Image.new('RGBA', large_size, (20, 24, 26, 255))
            background.paste(image,
                            ((large_size[0] - image.size[0]) / 2,
                            (large_size[1] - image.size[1]) / 2))
            output = StringIO()
            background.save(output, format='PNG', quality=75)
            output.seek(0)
            self.large_picture = InMemoryUploadedFile(output, 'ImageField',
                        image_name + '_large.png', 'image/png',
                        output.len, None)
            # Medium size
            background.thumbnail(medium_size, Image.ANTIALIAS)
            output = StringIO()
            background.save(output, format='PNG', quality=75)
            output.seek(0)
            self.medium_picture = InMemoryUploadedFile(output, 'ImageField',
                        image_name + '_medium.png', 'image/png',
                        output.len, None)
            # Small size
            background.thumbnail(small_size, Image.ANTIALIAS)
            output = StringIO()
            background.save(output, format='PNG', quality=75)
            output.seek(0)
            self.small_picture = InMemoryUploadedFile(output, 'ImageField',
                        image_name + '_small.png', 'image/png',
                        output.len, None)
            # Thumbnail size
            background.thumbnail(thumbnail_size, Image.ANTIALIAS)
            output = StringIO()
            background.save(output, format='PNG', quality=75)
            output.seek(0)
            self.thumbnail_picture = InMemoryUploadedFile(output, 'ImageField',
                        image_name + '_thumbnail.png', 'image/png',
                        output.len, None)
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return " ".join(filter(None, [self.name, self.surname]))

    def _picture_url(self, size='medium'):
        return S3URLValidator.get_public_url(self.picture, size)

    @property
    def picture_thumbnail(self):
        return self._picture_url('thumbnail')


class ImageUpload(models.Model):
    created = models.DateTimeField(editable=False, blank=True)
    modified = models.DateTimeField(editable=False, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(ImageUpload, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.__class__.__name__ + ":" + self.url

    def _picture_url(self, size='medium'):
        return S3URLValidator.get_public_url(self.url, size)

    @property
    def thumbnail(self):
        return self._picture_url('thumbnail')

    @property
    def medium(self):
        return self._picture_url('medium')
