from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Family


class UserRegisterForm(UserCreationForm):
    """用户注册表单"""

    email = forms.EmailField(required=True, label="电子邮箱")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "用户名",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义错误消息
        self.fields["password1"].help_text = "密码必须包含至少8个字符，不能是纯数字。"
        self.fields["username"].help_text = "用户名只能包含字母、数字和下划线。"


class UserProfileForm(forms.ModelForm):
    """用户档案表单"""

    class Meta:
        model = UserProfile
        fields = ["nickname", "avatar", "bio"]
        labels = {"nickname": "昵称", "avatar": "头像", "bio": "个人简介"}
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class FamilyForm(forms.ModelForm):
    """家庭创建表单"""

    class Meta:
        model = Family
        fields = ["name"]
        labels = {"name": "家庭名称"}
        help_texts = {"name": "请输入一个易于识别的家庭名称"}
