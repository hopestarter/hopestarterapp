from django.contrib.gis.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile

from hopespace.image import get_rotation

from time import time
from PIL import Image
from StringIO import StringIO

from hopespace.utils import geocode


def upload_image_to(instance, filename):
    return 'media/marks/%s/%s' % (instance.user.username, filename)


class LocationMark(models.Model):
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
    point = models.PointField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='marks')
    text = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    # Returns the string representation of the model.
    def __str__(self):
        return "<MARK:{}:{},{}:{}>".format(
            self.id, self.point.coords[0], self.point.coords[1],
            self.created.isoformat())

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        if self.picture:
            large_size = (800, 800)
            medium_size = (500, 500)
            small_size = (200, 200)
            thumbnail_size = (45, 45)
            # Use time stamp as integer for file name
            image_name = str(int(time()))
            # Resize and append
            image = Image.open(StringIO(self.picture.read()))
            rotation = get_rotation(image)
            if rotation is not None:
                image = image.transpose(rotation)
            image.thumbnail(large_size, Image.ANTIALIAS)
            background = Image.new('RGBA', image.size, (20, 24, 26, 255))
            background.paste(image)
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

        if self.point and (not self.country or not self.city):
            (city, state, country) = geocode(self.point.y, self.point.x)
            # Save the state if the city is not available
            self.city = city if city else state
            self.country = country

        super(LocationMark, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.__str__()


#class LocationImageUpload(models.Model):


class Ethnicity(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name_plural = "ethnicities"


    name = models.CharField(max_length=settings.ETHNICITY_MAX_NAME)
    people = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		through='EthnicMember',
		related_name='ethnicities')
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(Ethnicity, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class EthnicMember(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='membership')
    ethnicity = models.ForeignKey(Ethnicity, related_name='ethnicity')
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(EthnicMember, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s is in ethnic group %s" % (self.person, self.ethnicity)
