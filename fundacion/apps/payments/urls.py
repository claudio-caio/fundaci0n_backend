from django.urls import path
from .views import CreatePaymentView, MercadoPagoWebhook, PaymentStatusView

urlpatterns = [
    path("create/", CreatePaymentView.as_view()),
    path("webhook/", MercadoPagoWebhook.as_view()),
    path("status/<str:payment_id>/", PaymentStatusView.as_view()),
]
