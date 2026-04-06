from django.contrib import admin
from .models import product,Order
# Register your models here.
@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'image_url')
    search_fields = ('name', 'image_url')
    list_filter = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'total_price', 'created_at')
    search_fields = ('user__username', 'product__name', 'razorpay_order_id')
    list_filter = ('is_paid', 'created_at')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')