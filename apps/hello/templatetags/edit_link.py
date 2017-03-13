from django import template
from django.db.models.base import Model
from django.core.urlresolvers import reverse_lazy

register = template.Library()


@register.simple_tag
def edit_link(person):
    if not isinstance(person, Model):
        raise template.TemplateSyntaxError(
            "{} isn't correct object".format(person)
        )
    return reverse_lazy("admin:%s_%s_change" % (
        person._meta.app_label,
        person._meta.model_name
    ), args=(person.id,))
