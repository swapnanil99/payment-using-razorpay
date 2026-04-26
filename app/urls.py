from django.urls import path
from .views import AddToCartView
from .views import CartView
from .views import CartCheckoutView
from .views import CheckoutView
from .views import CreateCartPaymentView
from .views import CreatePaymentView
from .views import HomeView
from .views import PaymentFailedView
from .views import PaymentSuccessView
from .views import PaymentVerifyView
from .views import ProductListView
from .views import RemoveCartItemView
from .views import UpdateCartItemView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='cart_add'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='cart_update'),
    path('cart/remove/<int:product_id>/', RemoveCartItemView.as_view(), name='cart_remove'),
    path('checkout/cart/', CartCheckoutView.as_view(), name='checkout_cart'),
    path('checkout/<int:product_id>/', CheckoutView.as_view(), name='checkout'),
    path('create-payment/cart/', CreateCartPaymentView.as_view(), name='create_cart_payment'),
    path('create-payment/<int:product_id>/', CreatePaymentView.as_view(), name='create_payment'),
    path('payment-verify/', PaymentVerifyView.as_view(), name='payment_verify'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failed/', PaymentFailedView.as_view(), name='payment_failed'),
]