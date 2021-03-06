from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured

from actstream import settings
from actstream.signals import action


class ActstreamConfig(AppConfig):
    name = 'actstream'

    def ready(self):
        from actstream.actions import action_handler
        action.connect(action_handler, dispatch_uid='actstream.models')
        action_class = self.get_model('action')

        if settings.USE_JSONFIELD:
            try:
                if settings.USE_POSTGRES:
                    from django.contrib.postgres.fields import JSONField
                    JSONField(blank=True, null=True).contribute_to_class(action_class, 'data')
                else:
                    from jsonfield_compat import JSONField, register_app
                    JSONField(blank=True, null=True).contribute_to_class(action_class, 'data')
                    register_app(self)
            except ImportError:
                raise ImproperlyConfigured(
                    'You must have django-jsonfield and django-jsonfield-compat '
                    'installed if you wish to use a JSONField on your actions'
                )
