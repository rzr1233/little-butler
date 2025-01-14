from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import JsonResponse, Http404
from django.core.serializers.json import DjangoJSONEncoder
from .models import Account, Category, Bill, Budget
from .forms import AccountForm, BillForm
import json


class AccountListView(LoginRequiredMixin, ListView):
    """账本列表视图"""

    model = Account
    template_name = "bills/account_list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        # 获取用户拥有的和共享的账本
        personal_accounts = Account.objects.filter(
            owner=self.request.user, type="personal"
        ).select_related("owner")

        family_accounts = Account.objects.filter(
            family__members=self.request.user, type="family"
        ).select_related("owner", "family")

        return (personal_accounts | family_accounts).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["personal_accounts"] = [
            account for account in queryset if account.type == "personal"
        ]
        context["family_accounts"] = [
            account for account in queryset if account.type == "family"
        ]
        return context


class AccountCreateView(LoginRequiredMixin, CreateView):
    """创建账本视图"""

    model = Account
    form_class = AccountForm
    template_name = "bills/account_form.html"
    success_url = reverse_lazy("bills:account-list")

    def form_valid(self, form):
        account = form.save(commit=False)
        account.owner = self.request.user

        # 如果是家庭账本，设置关联的家庭
        if account.type == "family" and form.cleaned_data.get("family"):
            account.family = form.cleaned_data["family"]

        response = super().form_valid(form)

        # 创建默认分类
        default_categories = {
            "income": [
                {"name": "工资收入", "icon": "fas fa-money-bill-wave"},
                {"name": "投资收入", "icon": "fas fa-chart-line"},
                {"name": "其他收入", "icon": "fas fa-plus-circle"},
            ],
            "expense": [
                {"name": "餐饮美食", "icon": "fas fa-utensils"},
                {"name": "交通出行", "icon": "fas fa-car"},
                {"name": "购物消费", "icon": "fas fa-shopping-cart"},
                {"name": "住房物业", "icon": "fas fa-home"},
                {"name": "娱乐休闲", "icon": "fas fa-gamepad"},
                {"name": "医疗保健", "icon": "fas fa-hospital"},
                {"name": "教育培训", "icon": "fas fa-graduation-cap"},
                {"name": "其他支出", "icon": "fas fa-ellipsis-h"},
            ],
        }

        for type_name, categories in default_categories.items():
            for category_info in categories:
                Category.objects.create(
                    name=category_info["name"],
                    type=type_name,
                    account=account,
                    icon=category_info["icon"],
                )

        messages.success(self.request, "账本创建成功！")
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """更新账本视图"""

    model = Account
    form_class = AccountForm
    template_name = "bills/account_form.html"
    success_url = reverse_lazy("bills:account-list")

    def get_queryset(self):
        # 只能编辑自己创建的账本
        return Account.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "账本更新成功！")
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AccountDetailView(LoginRequiredMixin, DetailView):
    """账本详情视图"""

    model = Account
    template_name = "bills/account_detail.html"
    context_object_name = "account"

    def get_queryset(self):
        # 用户可以查看自己的账本和共享的家庭账本
        return Account.objects.filter(
            Q(owner=self.request.user) | Q(family__members=self.request.user)
        ).select_related("owner", "family")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.object

        # 添加账本统计信息
        bills = account.bills.select_related("category", "created_by")
        context["total_income"] = (
            bills.filter(type="income").aggregate(Sum("amount"))["amount__sum"] or 0
        )
        context["total_expense"] = (
            bills.filter(type="expense").aggregate(Sum("amount"))["amount__sum"] or 0
        )
        context["balance"] = context["total_income"] - context["total_expense"]
        context["recent_bills"] = bills.order_by("-date")[:5]

        # 检查用户权限
        context["is_owner"] = account.owner == self.request.user
        context["can_edit"] = context["is_owner"]
        if account.type == "family" and account.family:
            context["is_family_admin"] = account.family.familymember_set.filter(
                user=self.request.user, role="admin"
            ).exists()
            context["can_edit"] = context["can_edit"] or context["is_family_admin"]

        return context

    def handle_no_permission(self):
        messages.error(self.request, "你没有权限访问此账本")
        return redirect("bills:account-list")


class BillCreateView(LoginRequiredMixin, CreateView):
    """创建账单视图"""

    model = Bill
    form_class = BillForm
    template_name = "bills/bill_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.account = get_object_or_404(
            Account.objects.filter(
                Q(owner=self.request.user) | Q(family__members=self.request.user)
            ),
            pk=self.kwargs["account_pk"],
        )
        kwargs["account"] = self.account

        # 设置初始类型为支出
        if not kwargs.get("data"):  # 只在GET请求时设置初始值
            kwargs["initial"] = {"type": "expense"}

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = self.account

        # 将分类数据序列化为JSON
        if hasattr(context["form"], "all_categories"):
            context["form"].all_categories = {
                type_name: json.dumps(categories, cls=DjangoJSONEncoder)
                for type_name, categories in context["form"].all_categories.items()
            }

        return context

    def form_valid(self, form):
        bill = form.save(commit=False)
        bill.account = self.account
        bill.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "账单添加成功！")
        return response

    def get_success_url(self):
        return reverse_lazy("bills:account-detail", args=[self.account.pk])


@login_required
def get_account_categories(request, account_pk):
    """获取账本分类的API视图"""
    account = get_object_or_404(
        Account.objects.filter(Q(owner=request.user) | Q(family__members=request.user)),
        pk=account_pk,
    )

    bill_type = request.GET.get("type")
    if not bill_type:
        return JsonResponse({"error": "必须指定账单类型"}, status=400)

    categories = Category.objects.filter(account=account, type=bill_type).values(
        "id", "name", "icon"
    )

    return JsonResponse(list(categories), safe=False)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """删除账本视图"""

    model = Account
    success_url = reverse_lazy("bills:account-list")
    template_name = "bills/account_confirm_delete.html"

    def get_queryset(self):
        # 只能删除自己创建的账本
        return Account.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "账本删除成功！")
            return response
        except Exception as e:
            messages.error(request, f"删除账本失败：{str(e)}")
            return redirect("bills:account-list")


class BillUpdateView(LoginRequiredMixin, UpdateView):
    """编辑账单视图"""

    model = Bill
    form_class = BillForm
    template_name = "bills/bill_form.html"

    def get_queryset(self):
        # 用户可以编辑自己创建的账单，或者是自己所在家庭账本的账单
        return Bill.objects.filter(
            Q(created_by=self.request.user)
            | Q(account__family__members=self.request.user)
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["account"] = self.object.account
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = self.object.account
        # 将分类数据序列化为JSON
        if hasattr(context["form"], "all_categories"):
            context["form"].all_categories = {
                type_name: json.dumps(categories, cls=DjangoJSONEncoder)
                for type_name, categories in context["form"].all_categories.items()
            }
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "账单更新成功！")
        return response

    def get_success_url(self):
        return reverse_lazy("bills:account-detail", args=[self.object.account.pk])


class BillDeleteView(LoginRequiredMixin, DeleteView):
    """删除账单视图"""

    model = Bill
    template_name = "bills/bill_confirm_delete.html"

    def get_queryset(self):
        # 用户可以删除自己创建的账单，或者是自己所在家庭账本的账单
        return Bill.objects.filter(
            Q(created_by=self.request.user)
            | Q(account__family__members=self.request.user)
        )

    def get_success_url(self):
        return reverse_lazy("bills:account-detail", args=[self.object.account.pk])

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "账单删除成功！")
        return response
