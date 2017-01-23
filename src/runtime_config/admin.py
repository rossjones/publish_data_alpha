from django.contrib import admin

from runtime_config.models import ConfigProperty


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'active')
    list_filter = ('active',)


admin.site.register(ConfigProperty, ConfigAdmin)
