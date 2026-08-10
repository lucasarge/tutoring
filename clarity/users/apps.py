"""File for expanding the scope of an app sharing information with other apps."""

from django.apps import AppConfig

# Used to share signals between other apps.
class UsersConfig(AppConfig):
    name = 'users'
    def ready(self):
        import users.signals