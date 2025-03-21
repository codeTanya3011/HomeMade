from django.urls import path
from .views import PrivacyPolicyView, TermsAndConditionsView, DeliveryAndPaymentView, ContactInformationsView
from main import views


app_name = "main"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
    path('delivery_and_payment/', DeliveryAndPaymentView.as_view(), name='delivery_and_payment'),
    path('contact_informations/', ContactInformationsView.as_view(), name='contact_informations'),
]
