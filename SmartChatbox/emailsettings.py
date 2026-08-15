"""Email settings read from environment variables."""
import os

SET_EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
SET_EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
SET_EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
SET_EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
SET_EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
SET_EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend'
)
SET_DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', SET_EMAIL_HOST_USER)
