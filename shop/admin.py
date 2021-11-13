from django.contrib import admin
from django import forms
from django.forms import Textarea
from django.urls import reverse

from .models import Product, UserDetail, ProductSize, Cart, Wishlist, Rating, ProductQuery, ShippingCity, Contact, \
    OrderDetail, \
    OrderSummary, Notification, Cancellation, OrderUpdate, Dresse, Caste, DressColor, ProductDesigner, Event


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'size': forms.CheckboxSelectMultiple,
        }


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('id', 'name', 'dress_type', 'element_category', 'designer', 'caste_category', 'person_category', 'stock_size_s',
                    'stock_size_m',
                    'stock_size_l', 'stock_size_xl', 'stock_size_xxl', 'stock_size_3xl',
                    'pub_date')
    prepopulated_fields = {'slug': ('name', 'dress_type',)}


class CartAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user_id', 'product_id', 'product_name', 'caste_type', 'designer', 'dress_type', 'renting_way',
                    'product_size', 'quantity', 'amount', 'refund',
                    'renting_days', 'delivery_date', 'returning_date')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'user_id', 'user_name', 'product_id', 'caste_type', 'dress_type',
                    'product_size')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'product_id', 'ratings', 'review', 'posted_date')


class ProductQueryAdminForm(forms.ModelForm):
    class Meta:
        model = ProductQuery
        fields = '__all__'
        widgets = {
            'question': Textarea(attrs={'cols': 80, 'rows': 10}),
            'answer': Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class ProductQueryAdmin(admin.ModelAdmin):
    form = ProductQueryAdminForm
    list_display = ('product_name', 'product_id', 'user_name', 'question', 'answer', 'publish_date')


class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'first_name', 'last_name', 'email', 'address', 'contact', 'shipping_city',
                    'shipping_area', 'shipping_address')


class ShippingCityAdmin(admin.ModelAdmin):
    list_display = ('city', 'shipping_charge')


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'order_number', 'product_id', 'customer_name', 'customer_id', 'customer_user_name',
                    'customer_email',
                    'customer_contact',
                    'customer_address', 'caste_type', 'designer', 'dress_type', 'renting_way',
                    'product_size', 'quantity', 'amount', 'refund',
                    'renting_days', 'delivery_date', 'returning_date', 'shipping_address', 'shipping_charge',
                    'prod_image', 'ordered_date', 'order_status_date', 'payment_method', 'payment_status', 'order_status')


class OrderSummaryAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user_id', 'user_name', 'user_full_name', 'user_email', 'user_contact',
                    'total_items', 'sub_total_amount', 'total_refund', 'shipping_charge', 'grand_total',
                    'delivery_date', 'shipping_address', 'payment_method', 'payment_status', 'ordered_date', 'order_status',
                    'order_status_date')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user_id', 'total_items', 'order_status', 'order_status_date')


class CancellationAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_id', 'user_id', 'user_name', 'product_category', 'product_dress_type',
                    'image')


class DressAdmin(admin.ModelAdmin):
    list_display = ('dress', 'gender')


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_text', 'event_days', 'event_posted', 'event_status')


admin.site.register(Product, ProductAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(ProductSize)
admin.site.register(Cart, CartAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(ProductQuery, ProductQueryAdmin)
admin.site.register(ShippingCity, ShippingCityAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(OrderSummary, OrderSummaryAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Cancellation, CancellationAdmin)
admin.site.register(Dresse, DressAdmin)
admin.site.register(Caste)
admin.site.register(DressColor)
admin.site.register(ProductDesigner)
admin.site.register(Event, EventAdmin)
admin.site.register(Contact)
admin.site.register(OrderUpdate)
