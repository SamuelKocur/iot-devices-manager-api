from django.urls import path
from knox import views as knox_views


from . import views

urlpatterns = [
    path('login', views.LoginApiView.as_view(), name="login"),
    path('register', views.RegisterApiView.as_view(), name="register"),
    path('change-password', views.ChangePasswordApiView.as_view(), name="change-password"),

    path('logout/', knox_views.LogoutView.as_view()),
    path('logout-all/', knox_views.LogoutAllView.as_view()),
]
