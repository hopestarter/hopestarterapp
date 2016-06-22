from django.db import models
from django.conf import settings
from django.utils import timezone
from os.path import splitext

from hopebase.validators import S3URLValidator

def upload_image_to(instance, filename):
    filename_base, filename_ext = splitext(filename)
    print(filename_base)
    print(filename_ext)
    return 'media/users/%s/%s' % (instance.user.username, filename)


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    bitcoin = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(editable=False, blank=True)
    modified = models.DateTimeField(editable=False, blank=True)
    picture = models.ImageField(upload_to=upload_image_to, editable=True,
                    null=True, blank=True, max_length=255)
    # thumbnail = models.ImageField(upload_to=upload_image_to, editable=True,
                    # null=True, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
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
