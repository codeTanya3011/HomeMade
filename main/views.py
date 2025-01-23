from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = "Магазин мебели HomeMade"
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Про нас'
        context['content'] = "Про нас"
        context['text_on_page'] = "Наш мебельный магазин — это сочетание стиля, комфорта и качества. Мы предлагаем мебель, созданную для вашего уюта: от изысканных диванов до функциональных обеденных столов. Каждое изделие выполнено из качественных материалов и продумано до мелочей, чтобы радовать вас долгие годы. У нас вы найдёте стильные решения для любого интерьера, а опытные консультанты помогут выбрать то, что идеально подойдёт для вашего дома. Мы делаем ваш уют доступным!"
        return context


class PrivacyPolicyView(TemplateView):
    template_name = 'main/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = "HomeMade"
        return context


class TermsAndConditionsView(TemplateView):
    template_name = 'main/terms_and_conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = "HomeMade"
        return context


# def index(request) -> HttpResponse:

#     context = {
#         "title": "Home - Главная",
#         "content": "Магазин мебели Home",
#     }

#     return render(request, 'main/index.html', context)

# def about(request) -> HttpResponse:
#     context = {
#         "title": "Home - О нас",
#         "content": "О нашем магазине - Home",
#         "text_on_page": "Наш магазин очень классный и удобный вот увидете!"

#     }
    
#     return render(request, 'main/about.html', context)
