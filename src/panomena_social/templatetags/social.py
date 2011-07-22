from django import template
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

from panomena_general.exceptions import RequestContextRequiredException


register = template.Library()


class LikeNode(template.Node):
    """Tag for displaying like information and actions."""

    def __init__(self, obj, template):
        self.obj = obj
        self.template = template

    def render(self, context):
        # get the request object
        request = context.get('request', None)
        if request is None:
            raise RequestContextRequiredException()
        # resolve the arguments
        obj = self.obj.resolve(context)
        template = self.template.resolve(context)
        # render the template
        if hasattr(obj, 'is_liked'):
            liked = obj.is_liked(request)
        # get the content type of the object
        content_type = ContentType.objects.get_for_model(obj)
        # build context and render template
        return render_to_string(template, {
            'object': obj,
            'content_type': content_type,
            'liked': liked,
        })


@register.tag
def like(parser, token):
    bits = token.split_contents()
    # check for the right amount of arguments
    if len(bits) < 3:
        raise TemplateSyntaxError('%r takes at least 2 arguments' % bits[0])
    # parse the arguments
    obj = parser.compile_filter(bits[1])
    template = parser.compile_filter(bits[2])
    # build and return the node
    return LikeNode(obj, template)

