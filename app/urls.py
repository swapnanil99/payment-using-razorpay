from django.urls import path
from .views import CheckoutView
from .views import CreatePaymentView
from .views import HomeView
from .views import PaymentFailedView
from .views import PaymentSuccessView
from .views import PaymentVerifyView
from .views import ProductListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('checkout/<int:product_id>/', CheckoutView.as_view(), name='checkout'),
    path('create-payment/<int:product_id>/', CreatePaymentView.as_view(), name='create_payment'),
    path('payment-verify/', PaymentVerifyView.as_view(), name='payment_verify'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failed/', PaymentFailedView.as_view(), name='payment_failed'),
]