from django import template
from django.template import TemplateSyntaxError, RequestContext
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
        liked = False
        can_like = True
        # get the request object
        request = context.get('request', None)
        if request is None:
            raise RequestContextRequiredException()
        # resolve the arguments
        obj = self.obj.resolve(context)
        template = self.template.resolve(context)
        # get the leaf class of the object
        if hasattr(obj, 'as_leaf_class'):
            obj = obj.as_leaf_class()
        # check if the object is liked
        if hasattr(obj, 'is_liked'):
            liked = obj.is_liked(request)
        else:
            can_like = False
        # get the content type of the object
        content_type = ContentType.objects.get_for_model(obj)
        # build context and render template
        tag_context = RequestContext(request, {
            'object': obj,
            'content_type': content_type,
            'liked': liked,
            'can_like': can_like,
        })
        return render_to_string(template, tag_context)


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

