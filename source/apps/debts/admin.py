from django.contrib import admin
from source.apps.debts import models
from source.apps.receipts.services import ReceiptServices


class DebtAdmin(admin.ModelAdmin):

    search_fields = ['user__name', 'user__username', 'receipt__name']
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        ('receipt__created_at', admin.DateFieldListFilter),
    )


class DebtCalculationAdmin(admin.ModelAdmin):

    def save_model(self, request, obj: models.DebtCalculation, form, change) -> None:
        obj.save()
        ReceiptServices(obj.receipt).create_debts()


admin.site.register(models.DebtCalculation, DebtCalculationAdmin)
admin.site.register(models.Debt, DebtAdmin)
