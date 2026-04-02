from django.shortcuts import redirect, render
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services import GoogleOAuthService
from .models import SiteTheme
import json

oauth_service = GoogleOAuthService()

ALLOWED_COLORS = {
    "#fecdd3",  # Blush Rose
    "#fde68a",  # Golden Amber
    "#a7f3d0",  # Fresh Mint
    "#bae6fd",  # Ocean Sky
    "#c7d2fe",  # Royal Indigo
    "#ddd6fe",  # Soft Violet
    "#e2e8f0",  # Steel Slate
    "#fafaf9",  # Default
}

ALLOWED_FONTS = {
    "'Poppins', sans-serif",
    "'Playfair Display', serif",
    "'Dancing Script', cursive",
    "'Montserrat', sans-serif",
    "'Caveat', cursive",
    "'Oswald', sans-serif",
    "'DM Sans', sans-serif",   # default
}

def build_context(request):
    is_member = False
    if request.user.is_authenticated:
        is_member = request.user.email in settings.GROUP_MEMBERS

    theme = SiteTheme.get_solo()

    return {
        "is_member": is_member,
        "theme": theme,
    }

def show_main(request):
    return render(request, "main.html", build_context(request))

def start_google_login(request):
    return redirect(oauth_service.get_authorization_url())

def google_callback(request):
    code = request.GET.get("code")

    if not code:
        return redirect("main:show_main")

    tokens = oauth_service.get_tokens(code)
    if not tokens or "access_token" not in tokens:
        return redirect("main:show_main")

    user_data = oauth_service.get_user_info(tokens["access_token"])
    if not user_data or "email" not in user_data:
        return redirect("main:show_main")

    user, created = User.objects.get_or_create(
        email=user_data["email"],
        defaults={"username": user_data["email"].split("@")[0]},
    )

    django_login(request, user)
    return redirect("main:show_main")

def logout_view(request):
    if request.method == "POST":
        django_logout(request)
    return redirect("main:show_main")

def change_colour(request):
    if not request.user.is_authenticated:
        return render(request, "login_required.html", build_context(request))

    if request.user.email not in settings.GROUP_MEMBERS:
        return render(request, "not_member.html", build_context(request))

    return render(request, "warna.html", build_context(request))

def change_font(request):
    if not request.user.is_authenticated:
        return render(request, "login_required.html", build_context(request))

    if request.user.email not in settings.GROUP_MEMBERS:
        return render(request, "not_member.html", build_context(request))

    return render(request, "font.html", build_context(request))

@require_POST
def save_theme(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Harus login dulu"}, status=401)

    if request.user.email not in settings.GROUP_MEMBERS:
        return JsonResponse({"message": "Bukan anggota kelompok"}, status=403)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"message": "Body JSON tidak valid"}, status=400)

    theme = SiteTheme.get_solo()

    bg_color = data.get("bg_color")
    font_family = data.get("font_family")

    if bg_color is not None:
        if bg_color not in ALLOWED_COLORS:
            return JsonResponse({"message": "Warna tidak valid"}, status=400)
        theme.bg_color = bg_color

    if font_family is not None:
        if font_family not in ALLOWED_FONTS:
            return JsonResponse({"message": "Font tidak valid"}, status=400)
        theme.font_family = font_family

    theme.save()

    return JsonResponse({
        "message": "Theme berhasil disimpan",
        "bg_color": theme.bg_color,
        "font_family": theme.font_family,
    })