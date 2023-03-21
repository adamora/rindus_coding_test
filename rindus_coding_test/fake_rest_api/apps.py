from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FakeRestApiConfig(AppConfig):
    name = "rindus_coding_test.fake_rest_api"
    verbose_name = _("Fake Rest Api App")

    def ready(self):
        try:
            import rindus_coding_test.fake_rest_api.signals  # noqa F401
        except ImportError:
            pass
