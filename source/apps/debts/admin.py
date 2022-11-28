from django.contrib import admin
from django.db.transaction import atomic
from source.apps.debts import models
from source.apps.receipts.services import ReceiptServices


class DebtAdmin(admin.ModelAdmin):

    search_fields = ['user__name', 'user__username', 'receipt__name']
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        ('receipt__created_at', admin.DateFieldListFilter),
    )


class TotalDebtCalculationAdmin(admin.ModelAdmin):

    def save_model(self, request, obj: models.TotalDebtCalculation, form, change) -> None:
        obj.save()
        with atomic():
            models.TotalPersonalDebts.objects.calculate()


class DebtCalculationAdmin(admin.ModelAdmin):

    def save_model(self, request, obj: models.DebtCalculation, form, change) -> None:
        obj.save()
        receipt_service = ReceiptServices(obj.receipt)
        receipt_service.create_debts()
        receipt_service.create_personal_debts()


admin.site.register(models.DebtCalculation, DebtCalculationAdmin)
admin.site.register(models.TotalDebtCalculation, TotalDebtCalculationAdmin)
admin.site.register(models.Debt, DebtAdmin)
admin.site.register(models.PersonReceiptDebts)
admin.site.register(models.TotalPersonalDebts)
