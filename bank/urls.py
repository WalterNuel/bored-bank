from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomePage, name="index"),

    path("searchbar", views.searchbar, name="searchbar"),
    path("signup", views.signup, name="signup"),
    path("signin", views.login, name="signin"),
    path("logout", views.logout, name="logout"),

    path("deposit", views.deposit_screen, name="depo-screen"),
    path("deposit-acc", views.deposit_function, name="depo-func"),

    path("withdraw", views.withdraw_screen, name="withdraw-screen"),
    path("withdraw-acc", views.withdraw_function, name="withdraw-func"),

    path("send", views.send_screen, name="send"),
    path("send-func", views.send_func, name="send-func")
]
