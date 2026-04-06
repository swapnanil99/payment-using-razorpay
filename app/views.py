import base64
import hashlib
import hmac

import requests
from requests.exceptions import RequestException
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.models import Order
from app.models import product


def _get_or_create_payment_user(request):
    if request.user.is_authenticated:
        return request.user
    guest_user, _ = User.objects.get_or_create(
        username="guest_checkout",
        defaults={"email": "guest@example.com"},
    )
    return guest_user


def _basic_auth_header(key_id, key_secret):
    token = base64.b64encode(f"{key_id}:{key_secret}".encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {token}"}


class ProductListView(View):
    def get(self, request):
        return HomeView().get(request)


class HomeView(View):
    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        qs = product.objects.all().order_by("-id")
        if q:
            qs = qs.filter(name__icontains=q)

        return render(
            request,
            "product/home.html",
            {"products": qs, "q": q},
        )


class CheckoutView(View):
    def get(self, request, product_id):
        selected_product = get_object_or_404(product, id=product_id)
        return render(request, "product/checkout.html", {"product": selected_product})


@method_decorator(csrf_exempt, name="dispatch")
class CreatePaymentView(View):
    def post(self, request, product_id):
        if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
            return JsonResponse(
                {"error": "RAZORPAY_KEY_ID or RAZORPAY_KEY_SECRET is missing in environment."},
                status=500,
            )

        selected_product = get_object_or_404(product, id=product_id)
        payment_user = _get_or_create_payment_user(request)
        amount_paise = int(selected_product.price * 100)

        order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"product_{selected_product.id}_{payment_user.id}",
        }

        headers = {"Content-Type": "application/json"}
        headers.update(_basic_auth_header(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        session = requests.Session()
        # Avoid corporate/system proxy env vars interfering with local dev.
        session.trust_env = False
        try:
            response = session.post(
                "https://api.razorpay.com/v1/orders",
                json=order_data,
                headers=headers,
                timeout=20,
            )
        except RequestException as e:
            return JsonResponse(
                {"error": "Network error while contacting Razorpay", "details": str(e)},
                status=502,
            )

        if response.status_code not in (200, 201):
            return JsonResponse(
                {"error": "Unable to create Razorpay order", "details": response.text},
                status=502,
            )

        razorpay_order = response.json()
        Order.objects.create(
            user=payment_user,
            product=selected_product,
            quantity=1,
            amount=selected_product.price,
            total_price=selected_product.price,
            razorpay_order_id=razorpay_order["id"],
        )

        callback_url = request.build_absolute_uri(reverse("payment_verify"))
        return JsonResponse(
            {
                "order_id": razorpay_order["id"],
                "key": settings.RAZORPAY_KEY_ID,
                "key_id": settings.RAZORPAY_KEY_ID,
                "amount": amount_paise,
                "currency": "INR",
                "product_name": selected_product.name,
                "description": selected_product.description,
                "callback_url": callback_url,
            }
        )


@method_decorator(csrf_exempt, name="dispatch")
class PaymentVerifyView(View):
    def post(self, request):
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return redirect("payment_failed")

        body = f"{razorpay_order_id}|{razorpay_payment_id}".encode("utf-8")
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, razorpay_signature):
            return redirect("payment_failed")

        order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        order.is_paid = True
        order.save(update_fields=["razorpay_payment_id", "razorpay_signature", "is_paid"])

        return redirect("payment_success")


class PaymentSuccessView(View):
    def get(self, request):
        return render(request, "product/success.html")


class PaymentFailedView(View):
    def get(self, request):
        return render(request, "product/failed.html")
