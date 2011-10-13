from django.conf import settings
from django.shortcuts import redirect, get_object_or_404

from panomena_general.utils import is_ajax_request, json_response, \
    get_content_type

from panomena_social.models import Like, like_count


def like(request, content_type, pk):
    """Indicate that a user likes a content object."""
    user = request.user
    referer = request.META.get('HTTP_REFERER')
    # check if the user is authenticated
    if not user.is_authenticated():
        login_url = settings.LOGIN_URL + '?next=%s' % referer
        return redirect(login_url)
    # attempt to get the object
    content_type = get_content_type(content_type)
    obj = get_object_or_404(content_type.model_class(), pk=pk)
    # create the like
    like, created = Like.objects.get_or_create(
        user=user,
        object_pk=pk,
        content_type=content_type,
    )
    # respond to the request
    if is_ajax_request(request):
        return json_response({
            'success': created,
            'likes': like_count(obj),
        })
    else:
        next_url = request.REQUEST.get('next') or referer or '/'
        return redirect(next_url)


def unlike(request, content_type, pk):
    """Indicate that a user doesn't like an object."""
    user = request.user
    content_type = get_content_type(content_type)
    success = True
    # attempt to get the object
    obj = get_object_or_404(content_type.model_class(), pk=pk)
    # attempt to delete the like
    try:
        Like.objects.get(
            user=user,
            object_pk=pk,
            content_type=content_type,
        ).delete()
    except Like.DoesNotExist:
        success = False
    # respond to the request
    if is_ajax_request(request):
        return json_response({
            'success': success,
            'likes': like_count(obj),
        })
    else:
        next_url = request.REQUEST.get('next') or \
            request.META.get('HTTP_REFERER') or '/'
        return redirect(next_url)

