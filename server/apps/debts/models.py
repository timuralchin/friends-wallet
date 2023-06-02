from django.db import models

from server.apps.debts import managers, querysets
from server.apps.groups.models import Group, GroupMember
from server.apps.receipts.models import Receipt


class ReceiptDebt(models.Model):
    """Group member receipt total debt."""

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        blank=True,
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='debts',
    )
    group_member = models.ForeignKey(
        GroupMember,
        null=True,
        on_delete=models.SET_NULL,
        related_name='receipt_total_debs',
    )

    objects = querysets.ReceiptDebtQuerySet.as_manager()

    class Meta:
        unique_together = [['group_member', 'receipt']]
        verbose_name = 'Долг по чеку'
        verbose_name_plural = 'Долги по чеку'

    def __str__(self) -> str:
        return f'{self.group_member} debt by {self.receipt.name} with {self.amount} amount'


class TempDebts(models.Model):

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        blank=True,
        default=0,
    )
    debt = models.ForeignKey(
        ReceiptDebt,
        on_delete=models.CASCADE,
        related_name='temp',
    )

    def reduce(self, amount):
        self.amount -= amount
        self.save()

    def increase(self, amount):
        self.amount += amount
        self.save()


class GroupPersonalDebt(models.Model):
    """Total group personal debt model."""

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        blank=True,
        default=0,
    )
    debtor = models.ForeignKey(
        GroupMember,
        on_delete=models.CASCADE,
        related_name='total_debts',
    )
    creditor = models.ForeignKey(
        GroupMember,
        on_delete=models.CASCADE,
        related_name='total_credits',
    )
    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        related_name='debts',
    )

    objects = managers.GroupPersonalDebtsManager()

    class Meta:
        unique_together = [['debtor', 'creditor']]
        verbose_name = 'Личный долг в группе'
        verbose_name_plural = 'Личные долги в группе'

    def __str__(self) -> str:
        return f'{self.debtor} owes {self.creditor} {self.amount or 0} in {self.group} group'


class ReceiptPersonalDebt(models.Model):
    """Receipt personal debt."""

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        blank=True,
        default=0,
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='person_receipt_debs',
    )
    debtor = models.ForeignKey(
        GroupMember,
        on_delete=models.CASCADE,
        related_name='receipts_personal_debts',
    )
    creditor = models.ForeignKey(
        GroupMember,
        on_delete=models.CASCADE,
        related_name='receipts_personal_credits',
    )

    objects = managers.ReceiptPersonalDebtManager()

    class Meta:
        unique_together = [['debtor', 'creditor']]
        verbose_name = 'Личный долг по чеку'
        verbose_name_plural = 'Личные долги по чеку'

    def __str__(self) -> str:
        return f'{self.debtor} debt to {self.creditor} with {self.amount} on {self.receipt.name}'
