from django.urls import path, include
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    # path("sign-up/", views.sign_up, name="sign_up"),
]

