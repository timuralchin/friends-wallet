from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.core.mixins.models import CreatableMixin, UUIDMixin

User = get_user_model()


class Group(UUIDMixin, CreatableMixin, models.Model):
    """Group for members to share receipts."""

    name = models.CharField(max_length=255, verbose_name='Название')
    can_be_deleted = models.BooleanField()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.name


class GroupMember(models.Model):
    """Group member."""

    class Roles(models.TextChoices):
        """Member group roles."""
        CAN_EDIT = "CE", _("Can edit")
        VIEW_ONLY = "VO", _("View only")
        OWNER = "OW", _("Owner")

    name = models.CharField(max_length=255, blank=True, verbose_name='Имя')
    role = models.CharField(
        max_length=2,
        choices=Roles.choices,
        default=Roles.VIEW_ONLY,
        verbose_name='Роль',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Группа',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_memberships',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Участник группы'
        verbose_name_plural = 'Участники группы'

    def __str__(self) -> str:
        return self.name or self.user
