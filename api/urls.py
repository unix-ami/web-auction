"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
from . import views 
from .views import login_view, register_view
from django.urls import include, path

urlpatterns = [
    # path(''. main_spa),
    # path('', auth_redirect, name='auth-redirect'),
    # path('home/', main_spa, name='home'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('register/', register_view, name='register'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
    # path('api/user-email/', api_email_view, name='user-email'),
    # re_path(r'^(home|sell|auctions|bids|message|profile)/', main_spa, name='home'),
    # path('api/auth/login/', views.login_view, name='login'),
    # path('users/me/', profile_view, name='profile'),
    # path('api/csrf/', set_csrf_token, name='set-csrf-token'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('app/', views.main_spa, name='app'),
    path('app/', views.vue_app, name='vue_app'), 
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/profile/update/', views.update_profile, name='update_profile'),
    path('api/item/', views.create_item, name='create_item'),  # POST new item
    path('api/item/<int:item_id>/', views.item_detail, name='item_detail'), # view item
    path('api/items/', views.items_view, name='items_list'),  # GET all items
    path('api/item/<int:item_id>/bid/', views.place_bid, name='place_bid'),
    path('api/item/<int:item_id>/bids/', views.item_bids, name='item_bids'),
    path('api/bids/', views.user_bids, name='user_bids'),
    path('api/item/<int:item_id>/questions/', views.item_questions, name='item_questions'),
    path('api/item/<int:item_id>/ask/', views.ask_question, name='ask_question'),
    path('api/question/<int:question_id>/answer/', views.answer_question, name='answer_question'),
]