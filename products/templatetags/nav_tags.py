from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active_class(context, url_name):
    from django.urls import resolve
    try:
        return "active" if resolve(context['request'].path_info).url_name == url_name else ""
    except:
        return ""