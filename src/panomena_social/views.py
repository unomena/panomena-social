from django.shortcuts import redirect

from panomena_general.utils import is_ajax_request, json_response, \
    get_content_type

from panomena_social.models import Like


def like(request, content_type, pk):
    """Indicate that a user likes a content object."""
    user = request.user
    content_type = get_content_type(content_type)
    like, created = Like.objects.get_or_create(
        user=user,
        content_type=content_type,
        object_pk=pk
    )
    if is_ajax_request(request):
        return json_response({'success': created})
    else:
        next_url = request.REQUEST.get('next')
        return redirect(next_url)


def unlike(request, content_type, pk):
    """Indicate that a user doesn't like an object."""
    user = request.user
    content_type = get_content_type(content_type)
    success = True
    try:
        Like.objects.get(
            user=user,
            content_type=content_type,
            object_pk=pk
        ).delete()
    except Like.DoesNotExist:
        success = False
    if is_ajax_request(request):
        return json_response({'success': success})
    else:
        next_url = request.REQUEST.get('next')
        return redirect(next_url)

