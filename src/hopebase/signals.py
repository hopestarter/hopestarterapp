from django.dispatch import receiver
from django.db.models.signals import post_save

from hopespace.log import logger
from hopespace.models import LocationMark
from hopebase.util import increment_user_post_count


@receiver(post_save, sender=LocationMark)
def update_user_stats(sender, instance, created, **kwargs):
    if not instance:
        return
    # TODO check if instance should be hidden
    user = instance.user
    if created:
        try:
            increment_user_post_count(user)
        except Exception:
            logger.exception(
                "Couldn't increment post count for %s", user.username)
