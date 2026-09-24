from django.urls import path
from api.views import auth_view 

urlpatterns = [
    path('auth/login/', auth_view, name='login'),  # URL for the login view
]
