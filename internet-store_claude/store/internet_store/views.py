from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import OrderForm
from .models import Category, Order, OrderItem, Product

PER_PAGE = 12

SORTS = {
    "popular": ("За популярністю", "-reviews_count"),
    "new": ("Новинки", "-created"),
    "price_asc": ("Спочатку дешевші", "price"),
    "price_desc": ("Спочатку дорожчі", "-price"),
}

INFO_PAGES = {
    "about": "Про нас",
    "delivery": "Доставка та оплата",
    "returns": "Повернення та обмін",
    "contacts": "Контакти",
}


def _active_products():
    return Product.objects.filter(is_active=True).select_related("category")


def _back(request, fallback="index"):
    """Куди повернути користувача після POST-дії (лише на наш сайт)."""
    url = request.POST.get("next", "")
    if url and url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}):
        return redirect(url)
    return redirect(fallback)


def _listing(request, qs, *, title, breadcrumbs=(), subcategories=(), query=""):
    sort = request.GET.get("sort", "popular")
    if sort not in SORTS:
        sort = "popular"
    page = Paginator(qs.order_by(SORTS[sort][1], "pk"), PER_PAGE).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "catalog/product_list.html", {
        "title": title,
        "breadcrumbs": breadcrumbs,
        "subcategories": subcategories,
        "page": page,
        "sort": sort,
        "sorts": [(k, v[0]) for k, v in SORTS.items()],
        "query": query,
        "querystring": params.urlencode(),
    })


# ───────────── головна та каталог ─────────────

def index(request):
    hits = _active_products().filter(is_hit=True)
    tab = request.GET.get("c", "")
    hit_categories = Category.objects.filter(products__in=hits).distinct()
    if tab:
        hits = hits.filter(category__slug=tab)
    return render(request, "index.html", {
        "tiles": Category.objects.filter(parent__isnull=True, is_active=True),
        "hits": hits[:8],
        "hit_categories": hit_categories,
        "tab": tab,
    })


def catalog(request):
    query = request.GET.get("q", "").strip()
    qs = _active_products()
    if query:
        qs = qs.filter(name__icontains=query)
    title = f"Результати пошуку: «{query}»" if query else "Усі товари"
    return _listing(request, qs, title=title, query=query)


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug, is_active=True)
    qs = _active_products().filter(category_id__in=cat.family_ids())
    crumbs = [(cat.parent.name, cat.parent.get_absolute_url())] if cat.parent else []
    subs = cat.children.filter(is_active=True) if not cat.parent else cat.parent.children.filter(is_active=True)
    return _listing(request, qs, title=cat.name, breadcrumbs=crumbs, subcategories=subs)


def sale(request):
    qs = _active_products().filter(old_price__isnull=False)
    return _listing(request, qs, title="Акції та знижки")


def product_detail(request, slug):
    product = get_object_or_404(_active_products(), slug=slug)
    related = _active_products().filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, "catalog/product_detail.html", {"product": product, "related": related})


# ───────────── кошик ─────────────

def cart_detail(request):
    cart = Cart(request)
    lines = cart.lines()
    return render(request, "cart/cart.html", {"lines": lines, "total": cart.total(lines)})


@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True, in_stock=True)
    try:
        qty = max(1, int(request.POST.get("quantity", 1)))
    except ValueError:
        qty = 1
    Cart(request).add(product.pk, qty)
    messages.success(request, f"«{product.name}» додано до кошика")
    return _back(request)


@require_POST
def cart_update(request, pk):
    try:
        qty = int(request.POST.get("quantity", 1))
    except ValueError:
        qty = 1
    Cart(request).set(pk, qty)
    return redirect("cart")


@require_POST
def cart_remove(request, pk):
    Cart(request).remove(pk)
    return redirect("cart")


def checkout(request):
    cart = Cart(request)
    lines = cart.lines()
    if not lines:
        return redirect("cart")
    form = OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = form.save()
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=l["product"], name=l["product"].name,
                      price=l["product"].price, quantity=l["quantity"])
            for l in lines
        ])
        cart.clear()
        request.session["orders"] = [*request.session.get("orders", []), order.pk]
        return redirect("order_success", pk=order.pk)
    return render(request, "cart/checkout.html", {"form": form, "lines": lines, "total": cart.total(lines)})


def order_success(request, pk):
    if pk not in request.session.get("orders", []):
        raise Http404
    order = get_object_or_404(Order, pk=pk)
    return render(request, "cart/order_success.html", {"order": order})


# ───────────── бажане ─────────────

def wishlist(request):
    ids = request.session.get("wishlist", [])
    products = _active_products().filter(pk__in=ids)
    return render(request, "catalog/wishlist.html", {"products": products})


@require_POST
def wishlist_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    ids = list(request.session.get("wishlist", []))
    if product.pk in ids:
        ids.remove(product.pk)
    else:
        ids.append(product.pk)
    request.session["wishlist"] = ids
    return _back(request, "wishlist")


# ───────────── інформаційні сторінки ─────────────

def info_page(request, slug):
    if slug not in INFO_PAGES:
        raise Http404
    return render(request, f"pages/{slug}.html", {"title": INFO_PAGES[slug]})


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
