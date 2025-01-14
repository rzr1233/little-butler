from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import UserProfile, Family, FamilyMember
from .forms import UserRegisterForm, UserProfileForm, FamilyForm
from django.db import transaction


@transaction.atomic
def register_view(request):
    """用户注册视图"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 创建用户档案
            UserProfile.objects.create(user=user, nickname=user.username)
            messages.success(request, "注册成功！请登录。")
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    """用户档案视图"""
    # 如果用户没有档案，创建一个
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(
            user=request.user, nickname=request.user.username
        )

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "个人资料更新成功！")
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {"form": form})


class FamilyCreateView(LoginRequiredMixin, CreateView):
    """创建家庭视图"""

    model = Family
    form_class = FamilyForm
    template_name = "accounts/family_form.html"
    success_url = reverse_lazy("accounts:family-list")

    def form_valid(self, form):
        family = form.save(commit=False)
        family.creator = self.request.user
        response = super().form_valid(form)
        # 创建者自动成为管理员
        FamilyMember.objects.create(family=family, user=self.request.user, role="admin")
        messages.success(self.request, "家庭创建成功！")
        return response


class FamilyListView(LoginRequiredMixin, ListView):
    """家庭列表视图"""

    model = Family
    template_name = "accounts/family_list.html"
    context_object_name = "families"

    def get_queryset(self):
        return Family.objects.filter(members=self.request.user)


@login_required
def family_detail_view(request, pk):
    """家庭详情视图"""
    family = Family.objects.get(pk=pk)
    is_admin = family.familymember_set.filter(user=request.user, role="admin").exists()

    if request.method == "POST" and is_admin:
        # 处理添加成员的逻辑
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            FamilyMember.objects.create(family=family, user=user, role="member")
            messages.success(request, f"{username} 已添加到家庭。")
        except User.DoesNotExist:
            messages.error(request, f"用户 {username} 不存在。")
        except Exception as e:
            messages.error(request, str(e))
        return redirect("accounts:family-detail", pk=pk)

    return render(
        request, "accounts/family_detail.html", {"family": family, "is_admin": is_admin}
    )
