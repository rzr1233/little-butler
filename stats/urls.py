from django.urls import path
from . import views

app_name = "stats"

urlpatterns = [
    path("<int:account_id>/", views.StatsHomeView.as_view(), name="home"),
]
