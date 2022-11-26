from django.db import models
from source.apps.receipts.models import Receipt
from django.contrib.auth import get_user_model

User = get_user_model()


class DebtCalculation(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    receipt = models.OneToOneField(
        Receipt,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'{self.receipt} debt calculation'


class Debt(models.Model):

    amount = models.FloatField(null=True, blank=True, default=0)
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='debts',
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = [['user', 'receipt']]

    def __str__(self) -> str:
        return f'{self.user} debt by {self.receipt} with {self.amount} amount'


class PersonReceiptDebts(models.Model):

    amount = models.FloatField(null=True, blank=True, default=0)
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='person_receipt_debs',
    )
    debtor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receipts_debts',
    )
    creditor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receipts_credits',
    )

    def __str__(self) -> str:
        return f'{self.debtor} debt to {self.creditor} with {self.amount} on {self.receipt}'
