# Generated by Django 5.0.1 on 2025-01-14 15:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='账本名称')),
                ('type', models.CharField(choices=[('personal', '个人'), ('family', '家庭')], max_length=20, verbose_name='类型')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='accounts.family')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '账本',
                'verbose_name_plural': '账本',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='分类名称')),
                ('type', models.CharField(choices=[('expense', '支出'), ('income', '收入')], max_length=20, verbose_name='类型')),
                ('icon', models.CharField(blank=True, max_length=50, verbose_name='图标')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='bills.account')),
            ],
            options={
                'verbose_name': '账单分类',
                'verbose_name_plural': '账单分类',
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='预算金额')),
                ('start_date', models.DateField(verbose_name='开始日期')),
                ('end_date', models.DateField(verbose_name='结束日期')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='bills.account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.category')),
            ],
            options={
                'verbose_name': '预算',
                'verbose_name_plural': '预算',
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='金额')),
                ('type', models.CharField(choices=[('expense', '支出'), ('income', '收入')], max_length=20, verbose_name='类型')),
                ('date', models.DateField(verbose_name='日期')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='bills.account')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_bills', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bills.category')),
            ],
            options={
                'verbose_name': '账单',
                'verbose_name_plural': '账单',
                'ordering': ['-date', '-created_at'],
            },
        ),
    ]
