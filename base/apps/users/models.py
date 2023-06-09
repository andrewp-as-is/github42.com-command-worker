#from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.utils.crypto import salted_hmac
from django_passwordless_user.models import AbstractBaseUser

from base.apps.github.models import Token, User
from base.apps.github.utils import sync_user

class User(AbstractBaseUser):
    login = models.CharField(max_length=39,unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'

    class Meta:
        db_table = 'users_user'
        managed = False

    def get_absolute_url(self):
        return '/%s/' % self.login

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

def user_logged_in_handler(sender, user, request, **kwargs):
    # create github user
    User.objects.update_or_create({'login':user.login},id=user.id)
    # new token already active and not used
    token = Token.objects.get(user_id=request.user.id)
    # sync logged user
    sync_user(user.login,token)

user_logged_in.connect(user_logged_in_handler)
