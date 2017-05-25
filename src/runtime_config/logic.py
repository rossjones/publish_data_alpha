

from .models import ConfigProperty


def get_config(key):
    cp = ConfigProperty.objects.filter(key=key, active=True).first()
    return cp.value if cp else None
