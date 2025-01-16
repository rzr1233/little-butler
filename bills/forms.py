from django import forms
from .models import Account, Category, Bill, Budget
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta


class AccountForm(forms.ModelForm):
    """账本表单"""

    class Meta:
        model = Account
        fields = ["name", "type", "family", "description"]
        labels = {
            "name": "账本名称",
            "type": "账本类型",
            "family": "所属家庭",
            "description": "描述",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "给账本起个名字吧",
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "family": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "添加一些描述信息",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.user = user  # 保存user以供clean_name使用

        if user:
            # 只显示用户所在的家庭
            self.fields["family"].queryset = user.families.all()
            self.fields["family"].required = False

            # 添加帮助文本
            self.fields["type"].help_text = (
                "个人账本仅自己可见，家庭账本可与家庭成员共享"
            )
            self.fields["family"].help_text = "选择要共享账本的家庭（仅家庭账本需要）"

    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get("type")
        family = cleaned_data.get("family")

        if account_type == "family" and not family:
            raise forms.ValidationError({"family": "家庭账本必须选择所属家庭"})
        elif account_type == "personal" and family:
            cleaned_data["family"] = None

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get("name")
        user = self.user  # 从__init__中保存的user

        # 检查是否存在同名账本
        existing_account = (
            Account.objects.filter(Q(owner=user) | Q(family__members=user), name=name)
            .exclude(pk=self.instance.pk if self.instance else None)
            .first()
        )

        if existing_account:
            raise forms.ValidationError("你已经有一个同名的账本了，请换个名字")

        return name


class BillForm(forms.ModelForm):
    """账单表单"""

    class Meta:
        model = Bill
        fields = ["type", "amount", "category", "date", "description"]
        labels = {
            "type": "类型",
            "amount": "金额",
            "category": "分类",
            "date": "日期时间",
            "description": "备注",
        }
        widgets = {
            "type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "请输入金额",
                    "step": "0.01",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "添加备注信息",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        account = kwargs.pop("account", None)
        super().__init__(*args, **kwargs)

        if account:
            # 添加帮助文本
            self.fields["type"].help_text = "选择收入或支出"
            self.fields["category"].help_text = "选择交易分类"
            self.fields["date"].help_text = "选择或输入日期和时间"
            self.fields["date"].input_formats = [
                "%Y-%m-%dT%H:%M",
                "%Y-%m-%d %H:%M",
            ]

            # 设置日期默认值为当前时间（仅在初始加载时）
            if not self.instance.pk and not self.data:  # 确保只在初始加载时设置
                self.initial["date"] = timezone.now()

            # 预加载所有分类到内存中
            self.all_categories = {
                "income": list(
                    Category.objects.filter(account=account, type="income").values(
                        "id", "name"
                    )
                ),
                "expense": list(
                    Category.objects.filter(account=account, type="expense").values(
                        "id", "name"
                    )
                ),
            }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise forms.ValidationError("金额必须大于0")
        return amount

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if not date:
            raise forms.ValidationError("请选择或输入有效的日期和时间")
        return date


class BillSearchForm(forms.Form):
    """账单查询表单"""

    start_date = forms.DateField(
        label="开始日期",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    end_date = forms.DateField(
        label="结束日期",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    type = forms.ChoiceField(
        label="类型",
        choices=[("", "全部")] + Bill.TYPE_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    category = forms.CharField(
        label="分类",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "输入分类名称",
            }
        ),
    )

    keyword = forms.CharField(
        label="关键词",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "搜索备注信息",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("开始日期不能大于结束日期")

        return cleaned_data
