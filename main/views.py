from django.shortcuts import render

def show_main(request):
    return render(request, "main.html")

def show_warna(request):
    return render(request, "warna.html")