from django.contrib.auth import get_user_model
from django.db import models

from server.apps.groups.models import Group, GroupMember
from server.apps.receipts.models import Receipt


class GroupPersonalDebtsManager(models.Manager):

    def calculate(self):
        pass
        # for debtor in User.objects.all():
        #     creditors = User.objects.exclude(id=debtor.id).all()
        #     for creditor in creditors:
        #         debtor_amount = PersonReceiptDebts.objects.get_total_amount(
        #             debtor,
        #             creditor,
        #         )
        #         creditor_amount = PersonReceiptDebts.objects.get_total_amount(
        #             creditor,
        #             debtor,
        #         )
        #         delta_debt = abs(debtor_amount - creditor_amount)
        #         if debtor_amount >= creditor_amount:
        #             total_personal_debt, _ = self.update_or_create(
        #                 debtor=debtor,
        #                 creditor=creditor,
        #             )
        #             total_personal_debt.amount = delta_debt
        #             total_personal_debt.save()
        #             if old := self.filter(debtor=creditor, creditor=debtor).first():
        #                 old.delete()
        #         else:
        #             total_personal_debt, _ = self.update_or_create(
        #                 debtor=creditor,
        #                 creditor=debtor,
        #             )
        #             total_personal_debt.amount = delta_debt
        #             total_personal_debt.save()
        #             if old := self.filter(debtor=debtor, creditor=creditor).first():
        #                 old.delete()


class ReceiptPersonalDebtManager(models.Manager):
    """Receipt personal debt manager."""

    def get_total_amount(self, debtor, creditor):
        """Get total debt for two group members."""
        return self.filter(
            debtor=debtor,
            creditor=creditor,
        ).aggregate(models.Sum('amount')).get('amount__sum', 0) or 0
