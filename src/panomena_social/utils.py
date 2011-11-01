import hashlib


def generate_token(request):
    """Generates a token for a user or terminal."""
    # generate a terminal token
    token = '%s.%s' % (
        request.META['REMOTE_ADDR'],
        hashlib.md5(request.META['HTTP_USER_AGENT']).hexdigest(),
    )
    # append the user id if available
    user = request.user
    if user.is_authenticated():
        token += '.%s' % user.id
    # retunr the token
    return token
