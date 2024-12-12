from django.http import HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:
    context = {
        "title": "Home - Главная",
        "content": "Магазин мебели Home"
    }

    return render(request, 'main/index.html', context)

def about(request) -> HttpResponse:
    context = {
        "title": "Home - О нас",
        "content": "О нашем магазине - Home",
        "text_on_page": "Наш магазин очень классный и удобный вот увидете!"

    }
    
    return render(request, 'main/about.html', context)
