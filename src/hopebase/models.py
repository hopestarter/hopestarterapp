from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from StringIO import StringIO


def upload_image_to(instance, filename):
    return 'media/users/%s/%s' % (instance.user.username, filename)


class UserProfile(models.Model):
    MOBILE_APP = 'app'
    WEBAPP = 'web'
    NGO = 'ngo'
    SIGNUP_CHOICES = (
        (MOBILE_APP, 'app'),
        (WEBAPP, 'web'),
        (NGO, 'ngo'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    bitcoin = models.CharField(max_length=100, null=True, blank=True)
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
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    signup = models.SlugField(
        choices=SIGNUP_CHOICES,
        default=MOBILE_APP,
    )

    def picture_tag(self):
        return u'<a href="{}"><img src="{}" /></a>'.format(self.large_picture.url, self.small_picture.url)

    picture_tag.short_description = 'Picture'
    picture_tag.allow_tags = True

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        if self.picture:
            large_size = (800, 800)
            medium_size = (500, 500)
            small_size = (200, 200)
            thumbnail_size = (45, 45)

            # Get image name
            image_name = self.user.username
            image = Image.open(StringIO(self.picture.read()))

            # Large size
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
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return " ".join(filter(None, [self.name, self.surname]))


class UserStats(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='stats')
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    post_count = models.IntegerField(default=0)


class Organization(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='ownership')

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='OrganizationMembership',
        related_name='involved_orgs')

    vetted = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Vetting',
        related_name='vetted_by')

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(Organization, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class OrganizationMembership(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='involved')
    organization = models.ForeignKey(Organization, related_name='organization')
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    revoked = models.DateTimeField(null=True, blank=True)

    @property
    def valid(self):
        return self.revoked is not None

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(OrganizationMembership, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s is involved with the organization %s" % (
            self.person, self.organization
        )


class Vetting(models.Model):
    subject = models.ForeignKey(settings.AUTH_USER_MODEL)
    reviewer = models.ForeignKey(OrganizationMembership, null=True, blank=True)
    organization = models.ForeignKey(Organization)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    revoked = models.DateTimeField(null=True, blank=True)

    @property
    def valid(self):
        return self.revoked is not None

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(Vetting, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Organization {} vetted {} on {}".format(
            self.organization, self.subject, self.created) + \
            '(revoked on {})'.format(self.revoked) if not self.valid else ''
