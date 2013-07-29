from django import template
from django.contrib.contenttypes.models import ContentType
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
        raise template.TemplateSyntaxError(
            "%r tag requires exectly two argumments" % token.contents.split()[
                0])
    if not item:
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)
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
            cont_type = ContentType.objects.get_for_model(actual_item)
            object_admin_url = urlresolvers.reverse("admin:%s_%s_change" %
                                                    (cont_type.app_label,
                                                     cont_type.model),
                                                    args=(actual_item.pk,))
            return u'<a href="%s">(admin)</a>' % object_admin_url
        except template.VariableDoesNotExist:
            return ''
