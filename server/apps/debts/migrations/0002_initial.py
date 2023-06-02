# Generated by Django 4.1.3 on 2023-05-27 23:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        ('receipts', '0001_initial'),
        ('debts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptpersonaldebt',
            name='creditor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts_personal_credits', to='groups.groupmember'),
        ),
        migrations.AddField(
            model_name='receiptpersonaldebt',
            name='debtor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts_personal_debts', to='groups.groupmember'),
        ),
        migrations.AddField(
            model_name='receiptpersonaldebt',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_receipt_debs', to='receipts.receipt'),
        ),
        migrations.AddField(
            model_name='receiptdebt',
            name='group_member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receipt_total_debs', to='groups.groupmember'),
        ),
        migrations.AddField(
            model_name='receiptdebt',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts', to='receipts.receipt'),
        ),
        migrations.AddField(
            model_name='grouppersonaldebt',
            name='creditor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total_credits', to='groups.groupmember'),
        ),
        migrations.AddField(
            model_name='grouppersonaldebt',
            name='debtor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total_debts', to='groups.groupmember'),
        ),
        migrations.AddField(
            model_name='grouppersonaldebt',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='debts', to='groups.group'),
        ),
        migrations.AlterUniqueTogether(
            name='receiptdebt',
            unique_together={('group_member', 'receipt')},
        ),
        migrations.AlterUniqueTogether(
            name='grouppersonaldebt',
            unique_together={('debtor', 'creditor')},
        ),
    ]
