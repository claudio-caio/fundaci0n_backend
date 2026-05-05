from django.urls import path
from .views import RegisterView, login_view, user_detail_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('me/', user_detail_view, name='user_detail'),
]