from functools import cached_property
from uuid import uuid4

from django.db import models


class UUIDMixin(models.Model):
    """Table has UUID4 as primary key."""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        abstract = True


class CreatableMixin(models.Model):
    """Table has created_at field."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        abstract = True


class UpdatableMixin(models.Model):
    """Table has updated_at field."""

    updated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата обновления',
    )

    @cached_property
    def is_updated(self) -> bool:
        return self.updated_at is not None

    class Meta:
        abstract = True


class HistoricalMixin(CreatableMixin, UpdatableMixin):
    """Table has created_at & updated_at fields."""

    class Meta:
        abstract = True
