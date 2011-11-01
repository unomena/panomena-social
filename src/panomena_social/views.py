from django.shortcuts import redirect, get_object_or_404

from panomena_general.utils import is_ajax_request, json_response, \
    get_content_type

from panomena_social.models import Like, like_count
from panomena_social.utils import generate_token


def like(request, content_type, pk):
    """Indicate that a user likes a content object."""
    user = request.user
    content_type = get_content_type(content_type)
    # attempt to get the object
    obj = get_object_or_404(content_type.model_class(), pk=pk)
    # generate a token to identify the voting client
    token = generate_token(request)
    # create the like
    like, created = Like.objects.get_or_create(
        user=user if user.is_authenticated() else None,
        token=token,
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
        next_url = request.REQUEST.get('next') or \
            request.META.get('HTTP_REFERER') or '/'
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
        if user.is_authenticated():
            # delete the like attached to the user
            Like.objects.filter(
                user=user,
                object_pk=pk,
                content_type=content_type,
            ).delete()
        else:
            # delete the like attached to the terminal token
            Like.objects.filter(
                token=generate_token(request),
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

