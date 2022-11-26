from source.apps.receipts.models import Receipt
from source.apps.debts.models import Debt


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
