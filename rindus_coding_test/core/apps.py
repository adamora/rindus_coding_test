from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "rindus_coding_test.core"
    verbose_name = _("Core App")

    def ready(self):
        try:
            import rindus_coding_test.core.signals  # noqa F401
        except ImportError:
            pass
