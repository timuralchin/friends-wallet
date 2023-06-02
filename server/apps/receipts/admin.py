from django.contrib import admin

from server.apps.receipts import models


class PositionInline(admin.TabularInline):
    """Position inline for receipt admin."""

    model = models.Position
    extra = 0


class PayerInline(admin.TabularInline):
    """Payer inline for receipt admin."""

    model = models.Payer
    extra = 0


class ReceiptAdmin(admin.ModelAdmin):

    inlines = [PositionInline, PayerInline]
    exclude = ['updated_at']

    search_fields = ['name']
    list_display = ('name', 'total_amount', 'created_at', 'payers')

    def payers(self, obj: models.Receipt) -> list[str]:
        return [payer for payer in obj.payers.all()]


class CategoryAdmin(admin.ModelAdmin):
    """Category custom admin."""

    list_display = ('name', 'group', 'color')


admin.site.register(models.Receipt, ReceiptAdmin)
admin.site.register(models.Category, CategoryAdmin)
