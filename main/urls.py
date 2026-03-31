from django.urls import path
from main.views import show_main, show_warna

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('warna/', show_warna, name='show_warna'),
]