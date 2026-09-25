import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

logger = logging.getLogger('cloudstudent.security')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    request_id = getattr(request, 'request_id', 'unknown')
    logger.info(f"Successful login user={user.username} request_id={request_id}")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    request_id = getattr(request, 'request_id', 'unknown')
    # Credentials may contain passwords! Be extremely careful.
    # Only extract username safely.
    username = credentials.get('username', 'unknown')
    logger.warning(f"Failed login attempt username={username} request_id={request_id}")
