from django.db import models


class ReceiptDebtQuerySet(models.QuerySet):
    """Receipt debt queryset class."""

    def as_debts(self):
        """Filter as debts."""
        return self.filter(amount__gt=0)

    def as_credits(self):
        """Filter as credits."""
        return self.filter(amount__lt=0)
