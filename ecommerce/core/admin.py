from django.contrib import admin
from .models import Category, Product, ProductImage, Cart, Order, OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "added_at")
    search_fields = ("user__username", "product__name")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "get_total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    inlines = [OrderItemInline]

    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = "Total Price"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price")
    search_fields = ("order__id", "product__name")
