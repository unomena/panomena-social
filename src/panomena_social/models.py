from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from panomena_social.utils import generate_token


def is_liked(self, request):
    """Determines if an object has been liked by a user."""
    user = request.user
    content_type = ContentType.objects.get_for_model(self)
    # attempt to find like object
    try:
        if user.is_authenticated():
            # lookup the like by user
            Like.objects.get(
                user=request.user,
                object_pk=self.pk,
                content_type=content_type,
            )
        else:
            # lookup the like by the terminal token
            Like.objects.get(
                token=generate_token(request),
                object_pk=self.pk,
                content_type=content_type,
            )
        return True
    except Like.DoesNotExist:
        return False


def like_count(self):
    """Returns the amount of likes the object has."""
    content_type = ContentType.objects.get_for_model(self)
    return Like.objects.filter(
        content_type=content_type,
        object_pk=self.pk,
    ).count()


class Like(models.Model):
    """Model that represents a user liking an object."""

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='likes', blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_pk')

    def __unicode__(self):
        return '%s liked %s at %s' % (self.user, self.object, self.timestamp)
