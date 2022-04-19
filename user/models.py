from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, mobile, name, password=None, ** extra_fields):

        if not mobile:
            raise ValueError('Users must have a mobile number.')
        if not name:
            raise ValueError('Users must have a name.')
        # if not email:
        #     raise ValueError('Users must have an email address.')

        user = self.model(
            mobile=mobile,
            name=name,
            **extra_fields
        )

        if extra_fields['email']:
            user.email = self.normalize_email(extra_fields['email'])

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, mobile, name, password, ** extra_fields):
        """Create and save a new user"""
        return self._create_user(mobile, name, password,  ** extra_fields)

    def create_superuser(self, mobile, name, password, ** extra_fields):
        """Create and save a new superuser"""
        user = self._create_user(
            mobile, name, password, ** extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom authentication user model for authentication"""
    mobile_number_regex = RegexValidator(regex=r"^(\+?977)?\d{10}$")
    mobile = models.CharField(
        validators=[mobile_number_regex], max_length=14, unique=True)
    mobile_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=254, verbose_name=_('Full Name'))
    email = models.EmailField(
        max_length=255, blank=True, verbose_name=_("Recovery Email"))
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.name
