from django.urls import path
from mqtt import views

urlpatterns = [
    path('publish/', views.PublishApiView.as_view(), name='publish'),
]
