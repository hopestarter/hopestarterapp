from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from StringIO import StringIO


def upload_image_to(instance, filename):
    return 'media/users/%s/%s' % (instance.user.username, filename)


def resize(picture, sizes, name):
    """Returns a dict of InMemoryUploadedFile objects for each size."""

    uploaded_image = Image.open(StringIO(picture.read()))
    image = Image.new('RGBA', uploaded_image.size, (20, 24, 26, 255))
    image.paste(uploaded_image)

    pictures = {}
    for size in sizes:
        image.thumbnail(sizes[size], Image.ANTIALIAS)
        output = StringIO()
        image.save(output, format='PNG', quality=75)
        output.seek(0)
        pictures[size] = InMemoryUploadedFile(
            output, 'ImageField', "{}_{}.png".format(name, size),
            'image/png', output.len, None)
    return pictures


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
    PICTURE_OPTS = {
        "null": True, "blank": True, "max_length": 255,
        "upload_to": upload_image_to
    }
    picture = models.ImageField(**PICTURE_OPTS)
    large_picture = models.ImageField(editable=False, **PICTURE_OPTS)
    medium_picture = models.ImageField(editable=False, **PICTURE_OPTS)
    small_picture = models.ImageField(editable=False, **PICTURE_OPTS)
    thumbnail_picture = models.ImageField(editable=False, **PICTURE_OPTS)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    signup = models.SlugField(
        choices=SIGNUP_CHOICES,
        default=MOBILE_APP,
    )

    def picture_tag(self):
        return u'<a href="{}"><img src="{}" /></a>'.format(
            self.large_picture.url, self.small_picture.url)

    picture_tag.short_description = 'Picture'
    picture_tag.allow_tags = True

    @property
    def vetted(self):
        return self.user.vetting_set.filter(revoked=None).exists()

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        if self.picture:
            pictures = resize(self.picture, sizes={
                'large': (800, 800),
                'medium': (500, 500),
                'small': (200, 200),
                'thumbnail': (45, 45)
            }, name=self.user.username)
            self.large_picture = pictures['large']
            self.medium_picture = pictures['medium']
            self.small_picture = pictures['small']
            self.thumbnail_picture = pictures['thumbnail']
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
        return "%s (%s)" % (
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
        return self.revoked is None

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(Vetting, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} vetted by {} on {}".format(
            self.subject, self.organization, self.created)
