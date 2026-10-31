from .cart import Cart
from .models import Category


def shop(request):
    """Дані, потрібні на кожній сторінці (меню, лічильники у шапці)."""
    wishlist_ids = set(request.session.get("wishlist", []))
    return {
        "nav_categories": Category.objects.filter(parent__isnull=True, is_active=True),
        "cart_count": len(Cart(request)),
        "wishlist_ids": wishlist_ids,
        "wishlist_count": len(wishlist_ids),
    }
