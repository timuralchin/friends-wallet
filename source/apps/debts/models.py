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


class TotalDebtCalculation(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)


class DebtQuerySet(models.QuerySet):

    def as_debts(self):
        return self.filter(amount__gt=0)

    def as_credits(self):
        return self.filter(amount__lt=0)


class Debt(models.Model):

    amount = models.FloatField(null=True, blank=True, default=0)
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='debts',
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    objects = DebtQuerySet.as_manager()

    class Meta:
        unique_together = [['user', 'receipt']]

    def __str__(self) -> str:
        return f'{self.user} debt by {self.receipt} with {self.amount} amount'


class TempDebts(models.Model):

    amount = models.FloatField(null=True, blank=True, default=0)
    debt = models.ForeignKey(
        Debt,
        on_delete=models.CASCADE,
        related_name='temp',
    )

    def reduce(self, amount):
        self.amount -= amount
        self.save()

    def increase(self, amount):
        self.amount += amount
        self.save()


class TotalPersonalDebtsManager(models.Manager):

    def calculate(self):
        for debtor in User.objects.all():
            creditors = User.objects.exclude(id=debtor.id).all()
            for creditor in creditors:
                debtor_amount = PersonReceiptDebts.objects.get_total_amount(
                    debtor,
                    creditor,
                )
                creditor_amount = PersonReceiptDebts.objects.get_total_amount(
                    creditor,
                    debtor,
                )
                delta_debt = abs(debtor_amount - creditor_amount)
                if debtor_amount >= creditor_amount:
                    total_personal_debt, _ = self.update_or_create(
                        debtor=debtor,
                        creditor=creditor,
                    )
                    total_personal_debt.amount = delta_debt
                    total_personal_debt.save()
                    if old := self.filter(debtor=creditor, creditor=debtor).first():
                        old.delete()
                else:
                    total_personal_debt, _ = self.update_or_create(
                        debtor=creditor,
                        creditor=debtor,
                    )
                    total_personal_debt.amount = delta_debt
                    total_personal_debt.save()
                    if old := self.filter(debtor=debtor, creditor=creditor).first():
                        old.delete()


class TotalPersonalDebts(models.Model):

    amount = models.FloatField(null=True, blank=True, default=0)
    debtor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='total_debts',
    )
    creditor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='total_credits',
    )
    objects = TotalPersonalDebtsManager()

    class Meta:
        unique_together = [['debtor', 'creditor']]

    def __str__(self) -> str:
        return f'{self.debtor} owes {self.creditor} {self.amount or 0}'


class PersonalReceiptDebtsManager(models.Manager):

    def get_total_amount(self, debtor, creditor):
        return self.filter(debtor=debtor, creditor=creditor).aggregate(models.Sum('amount')).get('amount__sum', 0) or 0


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

    objects = PersonalReceiptDebtsManager()

    def __str__(self) -> str:
        return f'{self.debtor} debt to {self.creditor} with {self.amount} on {self.receipt}'
