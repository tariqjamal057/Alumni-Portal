from django import template

register = template.Library()


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.inclusion_tag("layouts/components/form_field.html")
def render_form_field(field, form_class="form-control", label_class="sr-only"):
    return {"field": field, "form_class": form_class, "label_class": label_class}
