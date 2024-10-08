# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import get_favorites
from .views import favicon_view


urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Home page
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='signup_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('add_favorite/<str:place_id>/<str:name>/<str:address>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<str:place_id>/', views.remove_favorite, name='remove_favorite'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('get_favorites/', get_favorites, name='get_favorites'),

    # Other routes
    path('favicon.jpg', favicon_view),
]