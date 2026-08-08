"""This file creates specified variables global."""

from django.conf import settings

# Sets variable GLOBAL_COST to what is stored in settings.GLOBAL_COST which is a constant for pricing.
def global_settings(request):
    return {
        'settings': {
            'GLOBAL_COST': settings.GLOBAL_COST
        }
    }