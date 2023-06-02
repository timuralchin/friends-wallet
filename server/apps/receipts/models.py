from typing import Iterable, Optional

from colorfield.fields import ColorField
from django.db import models

from server.apps.groups.models import Group, GroupMember
from server.apps.receipts import exceptions
from server.core.mixins.models import HistoricalMixin, UUIDMixin


class Receipt(UUIDMixin, HistoricalMixin, models.Model):
    """Receipt model."""

    name = models.CharField(
        blank=True,
        default='',
        max_length=255,
        verbose_name='Название',
    )
    total_amount = models.DecimalField(max_digits=15, decimal_places=3)
    participants = models.ManyToManyField(GroupMember, related_name='receipts')
    creator = models.ForeignKey(
        GroupMember,
        null=True,
        on_delete=models.SET_NULL,
        related_name='created_receipts',
    )
    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        related_name='receipts',
    )

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self) -> str:
        return f'{self.name} receipt created by {self.creator}'

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)


class Category(models.Model):
    """Position category."""

    name = models.CharField(max_length=255, verbose_name='Название')
    color = ColorField(default='#555555')
    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Группа',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return f'{self.name} ({self.group})'


class PositionManager(models.Manager):
    """Position model manager."""

    def get_total_amount(self):
        return self.aggregate(
            models.Sum('amount')
        ).get('amount__sum', 0)


class Position(models.Model):
    """Receipt position."""

    name = models.CharField(max_length=255, verbose_name='Название')
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name='Цена',
    )
    count = models.PositiveIntegerField(default=1,  verbose_name='Количество')
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name='Итоговая цена',
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name='Чек',
    )
    categories = models.ManyToManyField(Category, verbose_name='Категории')
    participants = models.ManyToManyField(
        GroupMember,
        verbose_name='Участники',
    )

    objects = PositionManager()

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self) -> str:
        return f"""{self.name} with {self.total_amount} total amount 
    ({self.amount} x {self.count}) in {self.receipt.name} receipt."""

    def save(self, *args, **kwargs):
        self.total_amount = max(self.total_amount, self.count * self.amount)
        return super().save(*args, **kwargs)


class Payer(models.Model):
    """Receipt payer model."""

    amount = models.DecimalField(max_digits=15, decimal_places=3)
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='payers',
    )
    group_member = models.ForeignKey(
        GroupMember,
        null=True,
        on_delete=models.SET_NULL,
        related_name='payments',
    )

    class Meta:
        verbose_name = 'Плательщик'
        verbose_name_plural = 'Плательщики'

    def __str__(self) -> str:
        return f'{self.group_member} payed {self.amount}'
