from django.shortcuts import redirect, render
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import User
from .services import GoogleOAuthService
from django.conf import settings

oauth_service = GoogleOAuthService()

def show_main(request):
    is_member = False
    if request.user.is_authenticated:
        is_member = request.user.email in settings.GROUP_MEMBERS
    return render(request, "main.html", {
        "is_member": is_member
    })

def start_google_login(request):
    return redirect(oauth_service.get_authorization_url())

def google_callback(request):
    code = request.GET.get('code')
    
    if not code:
        return redirect('main:show_main')

    tokens = oauth_service.get_tokens(code)
    if not tokens or 'access_token' not in tokens:
        return redirect('main:show_main')
    
    user_data = oauth_service.get_user_info(tokens['access_token'])
    if not user_data or 'email' not in user_data:
        return redirect('main:show_main')
    
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={'username': user_data['email'].split('@')[0]}
    )
    
    django_login(request, user)
    return redirect('main:show_main')

def logout_view(request):
    if request.method == "POST":
        django_logout(request)
    return redirect('main:show_main')

def change_colour(request):
    if not request.user.is_authenticated:
        return render(request, "login_required.html")
    
    if request.user.email not in settings.GROUP_MEMBERS:
        return render(request, "not_member.html")
        
    return render(request, "warna.html", {
        "is_member": True
    })

def change_font(request):
    if not request.user.is_authenticated:
        return render(request, "login_required.html")
    
    if request.user.email not in settings.GROUP_MEMBERS:
        return render(request, "not_member.html")
        
    return render(request, "font.html", {
        "is_member": True
    })