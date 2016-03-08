from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SysmoonConfig(AppConfig):
    name = "sysmoon"
    label = "sysmoon"
    verbose_name = _("Monitoring System")
