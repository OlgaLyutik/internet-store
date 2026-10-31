from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "emoji", "position", "is_active")
    list_editable = ("position", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("parent",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "old_price", "is_hit", "in_stock", "is_active")
    list_editable = ("price", "old_price", "is_hit", "in_stock", "is_active")
    list_filter = ("category", "is_hit", "is_active", "in_stock")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "name", "price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "phone", "city", "status", "created")
    list_editable = ("status",)
    list_filter = ("status", "delivery", "payment")
    search_fields = ("last_name", "phone", "email")
    inlines = [OrderItemInline]
