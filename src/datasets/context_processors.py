def govuk_overrides(request):
    from django.conf import settings
    return {
        'homepage_url': settings.HOMEPAGE_URL,
        'logo_link_title': settings.LOGO_LINK_TITLE,
        'global_header_text': settings.GLOBAL_HEADER_TEXT
    }
