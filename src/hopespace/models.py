from django.contrib.gis.db import models
from django.conf import settings


class LocationMark(models.Model):
    created = models.DateTimeField()
    point = models.PointField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='marks')

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return "<MARK:{}:{},{}:{}>".format(
            self.id, self.point.coords[0], self.point.coords[1],
            self.created.isoformat())
