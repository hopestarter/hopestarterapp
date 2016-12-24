from datetime import datetime

from django.db import IntegrityError
from django.db.models import F

from hopebase.models import UserStats
from hopebase.log import logger


def decrement_user_post_count(user):
    stats = UserStats.objects.filter(user=user)
    stats.update(
        post_count=F('post_count') - 1, modified=datetime.utcnow())


def increment_user_post_count(user):
    # this should be an upsert but django no support :(
    stats = UserStats.objects.filter(user=user)
    rows = stats.update(
        post_count=F('post_count') + 1, modified=datetime.utcnow())
    if rows == 0:
        try:
            UserStats(user=user, post_count=1).save()
        except IntegrityError:
            # TODO recalculate at a later point
            logger.exception(
                "Conflict while incrementing post count for %s",
                user.username)
