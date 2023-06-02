from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.users.exceptions import UserAlreadyJoined
from server.core.mixins.models import HistoricalMixin, UUIDMixin


class UserManager(DjangoUserManager):
    """Custom queryset for User model."""

    def create_user(self, email, **extra_fields):
        """Changed from username to email."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        username = extra_fields.get('username', None)
        user_exist = models.Q(email=email) | models.Q(username=username)
        if User.objects.filter(user_exist).exists():
            raise UserAlreadyJoined()

        return self._create_user(email, **extra_fields)

    def get_user_or_none(self, **kwargs):
        """Get user without exception."""
        try:
            return self.get(**kwargs)

        except self.model.DoesNotExist:
            return None

    def create_superuser(self, email=None, password=None, **extra_fields):
        """Override for email as username support."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password=None, **extra_fields):
        """Saved normalizing for login field."""
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label,
            self.model._meta.object_name,
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        if password is not None:
            user.password = make_password(password)

        user.save(using=self._db)
        return user


class User(UUIDMixin, HistoricalMixin, AbstractUser):
    """Custom user model."""

    first_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Фамилия',
    )
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        null=True,
        unique=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username or self.email
