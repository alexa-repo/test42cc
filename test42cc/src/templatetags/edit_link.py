from django import template
from django.core import urlresolvers

register = template.Library()

@register.tag(name="admin_link")
def edit_link_in_admin(parser, token):
    """
    This tag renders the link to its admin edit page for any object
    :param parser:
    :param token: get tag name and object, for it generate admin link
    :return:AdminEditLinkObject
    """
    try:
        print token
        tag_name, item = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exectly two argumments" %token.contents.split()[0])
    if not item:
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return AdminEditLink(item)


class AdminEditLink(template.Node):
    """
    return the link for admin edit page for object
    """
    def __init__(self, item):
        self.item = template.Variable(item)

    def render(self, context):
        try:
            actual_item = self.item.resolve(context)
            object_admin_url = urlresolvers.reverse("admin:%s_%s_change" % (actual_item._meta.app_label, actual_item._meta.module_name),
                                                    args=(actual_item.pk,))
            
            return object_admin_url
        except template.VariableDoesNotExist:
            return ''
