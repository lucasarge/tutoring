from django.conf import settings

def global_settings(request):
    return {
        'settings': {
            'GLOBAL_COST': settings.GLOBAL_COST
        }
    }