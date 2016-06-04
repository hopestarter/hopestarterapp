from django.db import models
from django.conf import settings
from django.utils import timezone


from hopebase.validators import S3URLValidator


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    bitcoin = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(editable=False, blank=True)
    modified = models.DateTimeField(editable=False, blank=True)
    picture = models.URLField(max_length=200, null=True, blank=True)

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
