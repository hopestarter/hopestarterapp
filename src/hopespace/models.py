from django.contrib.gis.db import models
from django.conf import settings
from django.utils import timezone

from hopebase.models import ImageUpload


class LocationMark(models.Model):
    created = models.DateTimeField()
    point = models.PointField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='marks')
    text = models.TextField(null=True, blank=True)


    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return "<MARK:{}:{},{}:{}>".format(
            self.id, self.point.coords[0], self.point.coords[1],
            self.created.isoformat())


class LocationImageUpload(ImageUpload):
    mark = models.ForeignKey(LocationMark, related_name='picture')


class Ethnicity(models.Model):
    class Meta(object):
        ordering = ['name']
        verbose_name_plural = "ethnicities"


    name = models.CharField(max_length=settings.ETHNICITY_MAX_NAME)
    people = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		through='EthnicMember',
		related_name='ethnicities')
    created = models.DateTimeField(editable=False, blank=True)
    modified = models.DateTimeField(editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Ethnicity, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class EthnicMember(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='membership')
    ethnicity = models.ForeignKey(Ethnicity, related_name='ethnicity')
    created = models.DateTimeField(editable=False, blank=True)
    modified = models.DateTimeField(editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(EthnicMember, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s is in ethnic group %s" % (self.person, self.ethnicity)
