
from django.urls import path
from .api.user import views

urlpatterns = [
    path('user/login/', views.UserLoginView, name='user_login'),
]