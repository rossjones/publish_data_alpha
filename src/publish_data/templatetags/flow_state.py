from django import template

register = template.Library()


@register.filter
def is_editing(request):
    return request.session.get('flow-state') == 'editing'


@register.filter
def is_checking(request):
    return request.session.get('flow-state') == 'checking'


@register.filter
def clear_flow_state(request):
    previous = request.session.get('flow-state', '')
    request.session['flow-state'] = None
    return previous or ''
