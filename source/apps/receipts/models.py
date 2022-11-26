from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Receipt(models.Model):

    name = models.CharField(blank=True, default='', max_length=255)
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    subjects = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f'{self.name} receipt'


class PositionManager(models.Manager):

    def get_total_amount(self):
        return self.aggregate(
            models.Sum('amount')
        ).get('amount__sum', 0)


class Position(models.Model):

    amount = models.FloatField()
    name = models.CharField(max_length=255)
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='positions',
    )
    subjects = models.ManyToManyField(User)

    objects = PositionManager()


class Payer(models.Model):

    amount = models.FloatField()
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='payers',
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.user} payed {self.amount}'
