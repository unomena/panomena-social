from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Like(models.Model):
    """Model that represents a user liking an object."""

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='likes')
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_pk')

    def __unicode__(self):
        return '%s liked %s at %s' % (self.user, self.object, self.timestamp)
