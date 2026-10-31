from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # каталог
    path("catalog/", views.catalog, name="catalog"),            # усі товари + пошук ?q=
    path("catalog/<slug:slug>/", views.category, name="category"),
    path("sale/", views.sale, name="sale"),
    path("product/<slug:slug>/", views.product_detail, name="product"),

    # кошик і замовлення
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:pk>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:pk>/success/", views.order_success, name="order_success"),

    # бажане
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/toggle/<int:pk>/", views.wishlist_toggle, name="wishlist_toggle"),

    # інформаційні сторінки: about, delivery, returns, contacts
    path("info/<slug:slug>/", views.info_page, name="page"),
]
