from django.urls import path
from knox import views as knox_views

import user_auth.views.user_updates as profile_update_views
import user_auth.views.auth as auth_views

urlpatterns = [
    path('login/', auth_views.LoginApiView.as_view(), name="login"),
    path('register/', auth_views.RegisterApiView.as_view(), name="register"),
    path('logout/', knox_views.LogoutView.as_view(), name="logout"),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name="logout-from-all-devices"),

    path('change-password/', profile_update_views.ChangePasswordApiView.as_view(), name="change-password"),
    path('profile/', profile_update_views.UpdateUserProfileApiView.as_view(), name="update-profile"),
    path('app-settings/', profile_update_views.UserAppSettingsView.as_view(), name="customize_user_app_settings"),

    path('delete-account/', auth_views.DeleteUserApiView.as_view(), name="update-profile"),

    path('validate-token/', auth_views.CheckTokenView.as_view(), name='check-token-validity'),
]
