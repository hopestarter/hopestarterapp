from django.db import models
from django.conf import settings
from django.utils import timezone


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
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
        return self.__class__.name + ":" + self.url
