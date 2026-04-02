from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('auth/login/', views.start_google_login, name='google_login'),
    path('auth/callback/', views.google_callback, name='google_callback'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/warna/', views.change_colour, name='change_colour'),
    path('auth/font/', views.change_font, name='change_font'),
    path('auth/theme/save/', views.save_theme, name='save_theme'),
]