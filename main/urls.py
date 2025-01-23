from django.urls import path
from .views import PrivacyPolicyView, TermsAndConditionsView
from main import views

app_name = "main"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
]
