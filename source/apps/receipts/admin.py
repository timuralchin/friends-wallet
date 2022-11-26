from django.contrib import admin
from source.apps.receipts import models
from source.apps.debts.models import Debt
from django.db.models import Sum


class PositionAdmin(admin.TabularInline):

    model = models.Position
    extra = 0


class PayerAdmin(admin.TabularInline):

    model = models.Payer
    extra = 1


class ReceiptAdmin(admin.ModelAdmin):

    inlines = [PositionAdmin, PayerAdmin]

    search_fields = ['name']


admin.site.register(models.Receipt, ReceiptAdmin)
