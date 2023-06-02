from django.contrib import admin

from server.apps.debts import models

admin.site.register(models.ReceiptDebt)
admin.site.register(models.ReceiptPersonalDebt)
admin.site.register(models.GroupPersonalDebt)
