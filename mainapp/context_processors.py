from django.conf import settings


def google_maps_settings(request):
    """Expose the browser-restricted Google Maps key to Django templates."""
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
