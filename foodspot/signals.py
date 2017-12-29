from django.conf import settings
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import foodspot.models as models

@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_token_for_new_user")
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     print("Request finished!")
