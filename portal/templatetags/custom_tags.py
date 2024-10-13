from django import template

from portal.utils import is_alumni as alumni
from portal.utils import is_faculty as faculty
from portal.utils import is_student as student

register = template.Library()


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.inclusion_tag("layouts/components/form_field.html")
def render_form_field(field, form_class="form-control", label_class="sr-only"):
    return {"field": field, "form_class": form_class, "label_class": label_class}


@register.filter
def is_student(user):
    return student(user)


@register.filter
def is_alumni(user):
    return alumni(user)


@register.filter
def is_faculty(user):
    return faculty(user)
