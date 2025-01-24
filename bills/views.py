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
from .forms import AccountForm, BillForm, BillSearchForm
import json
from decimal import Decimal
from django.core.paginator import Paginator
from datetime import datetime, timedelta


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
    paginate_by = 20  # 每页显示20条账单

    def get_queryset(self):
        # 用户可以查看自己的账本和共享的家庭账本
        base_query = Account.objects.select_related("owner", "family")

        # 获取用户所属的所有家庭ID
        user_family_ids = self.request.user.families.values_list("id", flat=True)

        return base_query.filter(
            Q(owner=self.request.user)  # 用户自己的账本
            | Q(type="family", family__id__in=user_family_ids)  # 用户所属家庭的账本
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.object

        # 处理搜索表单
        form = BillSearchForm(self.request.GET)
        context["search_form"] = form

        # 获取账单查询集
        bills = account.bills.select_related("category", "created_by")

        # 如果表单有效，应用过滤条件
        if form.is_valid():
            # 日期过滤
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date:
                bills = bills.filter(date__date__gte=start_date)
            if end_date:
                bills = bills.filter(date__date__lte=end_date)

            # 类型过滤
            bill_type = form.cleaned_data.get("type")
            if bill_type:
                bills = bills.filter(type=bill_type)

            # 分类过滤
            category = form.cleaned_data.get("category")
            if category:
                bills = bills.filter(category__name__icontains=category)

            # 关键词过滤
            keyword = form.cleaned_data.get("keyword")
            if keyword:
                bills = bills.filter(description__icontains=keyword)

        # 计算统计信息（基于过滤后的查询集）
        context["total_income"] = round(
            bills.filter(type="income").aggregate(Sum("amount"))["amount__sum"]
            or Decimal("0"),
            2,
        )
        context["total_expense"] = round(
            bills.filter(type="expense").aggregate(Sum("amount"))["amount__sum"]
            or Decimal("0"),
            2,
        )
        context["balance"] = round(
            context["total_income"] - context["total_expense"], 2
        )

        # 分页处理
        bills_list = bills.order_by("-date")
        paginator = Paginator(bills_list, self.paginate_by)
        page = self.request.GET.get("page", 1)
        context["recent_bills"] = paginator.get_page(page)

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
            self.object = self.get_object()

            # 检查是否有关联的账单，并尝试删除
            bills_count = self.object.bills.count()
            if bills_count > 0:
                try:
                    # 先删除所有关联的账单
                    self.object.bills.all().delete()
                except Exception as e:
                    messages.error(
                        request,
                        f"删除账单记录时出错：{str(e)}",
                    )
                    return redirect("bills:account-detail", pk=self.object.pk)

            # 删除关联的分类
            try:
                self.object.categories.all().delete()
            except Exception as e:
                messages.error(
                    request,
                    f"删除分类时出错：{str(e)}",
                )
                return redirect("bills:account-detail", pk=self.object.pk)

            # 最后删除账本
            self.object.delete()
            messages.success(request, "账本删除成功！")
            return redirect(self.success_url)

        except Exception as e:
            messages.error(request, f"删除账本时出错：{str(e)}")
            return redirect("bills:account-list")


class BillCreateView(LoginRequiredMixin, CreateView):
    """创建账单视图"""

    model = Bill
    form_class = BillForm
    template_name = "bills/bill_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        # 获取账本并检查权限
        account_pk = self.kwargs.get("account_pk")
        if not account_pk:
            raise Http404("未指定账本")

        try:
            # 检查用户是否有权限访问该账本
            self.account = Account.objects.get(pk=account_pk)

            # 检查权限
            if self.account.type == "personal":
                # 个人账本只能由所有者访问
                if self.account.owner != self.request.user:
                    raise Http404("你没有权限访问此账本")
            else:
                # 家庭账本需要检查用户是否是家庭成员
                if not self.account.family.familymember_set.filter(
                    user=self.request.user
                ).exists():
                    raise Http404("你不是此家庭账本的成员")

            kwargs["account"] = self.account

            # 设置初始类型为支出
            if not kwargs.get("data"):
                kwargs["initial"] = {"type": "expense"}

            return kwargs
        except Account.DoesNotExist:
            raise Http404("账本不存在")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = self.account
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
        # 获取基础查询集，预加载必要的关联数据
        base_queryset = Bill.objects.select_related(
            "account", "account__family", "category", "created_by"
        )

        # 用户可以删除：
        # 1. 自己创建的账单
        # 2. 自己所在家庭账本的账单（需要是家庭成员）
        return base_queryset.filter(
            Q(created_by=self.request.user)  # 自己创建的账单
            | Q(  # 家庭账本的账单（需要是家庭成员）
                account__type="family",
                account__family__familymember_set__user=self.request.user,
            )
        )

    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
            # 保存账本ID，以防删除后需要重定向
            self.account_id = obj.account.id
            return obj
        except Http404:
            messages.error(self.request, "找不到要删除的账单或没有删除权限")
            return None
        except Exception as e:
            messages.error(self.request, f"获取账单时出错：{str(e)}")
            return None

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if not self.object:
                return redirect("bills:account-list")

            # 保存账本ID用于重定向
            account_id = self.object.account.id

            # 执行删除
            self.object.delete()
            messages.success(request, "账单删除成功！")
            return redirect("bills:account-detail", pk=account_id)

        except Exception as e:
            messages.error(request, f"删除账单时出错：{str(e)}")
            try:
                # 尝试重定向到账本详情页
                if hasattr(self, "account_id"):
                    return redirect("bills:account-detail", pk=self.account_id)
            except:
                pass
            # 如果获取账本ID失败，返回账本列表
            return redirect("bills:account-list")
