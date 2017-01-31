from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('includes/analytics.html')
def analytics():
    return {
        'analytics_code': settings.ANALYTICS_ID
    }
