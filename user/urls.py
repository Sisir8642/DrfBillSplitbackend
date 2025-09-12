from django.urls import path
from .views import RegisterView, LoginView 
from .views import current_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/me/', current_user, name='current-user'),
]
