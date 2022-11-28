from source.apps.receipts.models import Receipt
from source.apps.debts.models import Debt, TempDebts, PersonReceiptDebts


class ReceiptServices:

    def __init__(self, receipt: Receipt) -> None:
        self.receipt = receipt
        self.calc_base_payer_amount()

    def create_debts(self):
        for subject in self.receipt.subjects.all():
            debt, _ = Debt.objects.get_or_create(
                user=subject,
                receipt=self.receipt,
            )
            subject_positions = self.receipt.positions.filter(
                subjects__id=subject.id,
            ).all()

            debt_amount = self.base_amount + \
                self.get_subject_position_debt_amount(subject_positions)
            if payer := self.receipt.payers.filter(user=subject).first():
                debt_amount -= payer.amount

            debt.amount = round(debt_amount, 2)
            debt.save()

    def calc_base_payer_amount(self) -> None:
        self.base_amount = self.receipt.total_amount

        if positions_amount := self.receipt.positions.get_total_amount():
            self.base_amount -= positions_amount

        if subjects_count := self.receipt.subjects.count():
            self.base_amount /= subjects_count

    def get_subject_position_debt_amount(self, positions):
        debt_amount = 0
        for position in positions:
            debt_amount += position.amount / position.subjects.count()
        return debt_amount

    def create_personal_debts(self):
        debts = self.receipt.debts.as_debts()
        credits = self.receipt.debts.as_credits()
        temp_credits = TempDebts.objects.bulk_create(
            [
                TempDebts(debt=credit, amount=credit.amount)
                for credit in credits
            ]
        )
        for debt in debts:
            temp_debt = TempDebts.objects.create(
                debt=debt,
                amount=debt.amount
            )
            for temp_credit in temp_credits:
                temp_amount = min(temp_debt.amount, abs(temp_credit.amount))
                if temp_amount == 0:
                    continue
                temp_debt.reduce(temp_amount)
                temp_credit.increase(temp_amount)
                PersonReceiptDebts.objects.update_or_create(
                    amount=temp_amount,
                    receipt=self.receipt,
                    debtor=debt.user,
                    creditor=temp_credit.debt.user,
                )
                if temp_debt.amount <= 0:
                    temp_debt.delete()
                    break
        TempDebts.objects.filter(debt__in=credits).delete()
