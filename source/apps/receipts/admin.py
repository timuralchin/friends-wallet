from django.contrib import admin
from source.apps.receipts import models


class PositionAdmin(admin.TabularInline):

    model = models.Position
    extra = 0


class PayerAdmin(admin.TabularInline):

    model = models.Payer
    extra = 1


class ReceiptAdmin(admin.ModelAdmin):

    inlines = [PositionAdmin, PayerAdmin]

    search_fields = ['name']
    list_display = ('name', 'total_amount', 'created_at', 'payers')

    def payers(self, obj: models.Receipt) -> list[str]:
        return [payer for payer in obj.payers.all()]


admin.site.register(models.Receipt, ReceiptAdmin)
