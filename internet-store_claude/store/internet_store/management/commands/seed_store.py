from django.core.management.base import BaseCommand

from internet_store.models import Category, Product

# (slug, назва, емодзі, [підкатегорії])
CATEGORIES = [
    ("sypalnya", "Спальня", "🛏️", [("podushky", "Подушки"), ("kovdry", "Ковдри"), ("bilyzna", "Білизна")]),
    ("vanna", "Ванна кімната", "🛁", []),
    ("domashniy-odyag", "Домашній одяг", "👘", []),
    ("dytyachi", "Дитячі товари", "🧸", []),
    ("kuhnya", "Кухня", "🍽️", []),
    ("premium", "Преміум", "⭐", []),
    ("outlet", "Outlet", "🏷️", []),
]

# (slug, назва, емодзі, ціна, стара ціна, відгуки, підкатегорія, колір)
PRODUCTS = [
    ("podushka-comfort", "Подушка антиалергенна Comfort", "🛏️", 439, 665, 38, "podushky", "#cfe0ff"),
    ("podushka-premium", "Подушка ортопедична Premium", "💤", 529, 802, 26, "podushky", "#d9f2e6"),
    ("podushka-extra", "Подушка пухова Extra", "☁️", 1296, 2057, 27, "podushky", "#fde7c8"),
    ("kovdra-eco", "Ковдра антиалергенна Eco", "🧺", 1297, 6485, 33, "kovdry", "#e6dcff"),
    ("kovdra-gold", "Ковдра вовняна Gold", "🐑", 934, 1394, 9, "kovdry", "#fdd9dc"),
    ("kovdra-kasetna", "Ковдра пухова касетна", "🪶", 3697, 6846, 96, "kovdry", "#d6f0f7"),
    ("bilyzna-stripe", "Комплект білизни Stripe", "🛌", 999, 1638, 20, "bilyzna", "#cfe0ff"),
    ("bilyzna-light-gray", "Комплект білизни Light Gray", "🛌", 999, 1693, 36, "bilyzna", "#e4e6ee"),
    ("bilyzna-ranforce", "Комплект білизни Ranforce", "🛌", 1199, 1903, 42, "bilyzna", "#d9f2e6"),
]


class Command(BaseCommand):
    help = "Наповнює магазин початковими категоріями та товарами (дані зі старого script.js)"

    def handle(self, *args, **options):
        for pos, (slug, name, emoji, subs) in enumerate(CATEGORIES):
            parent, _ = Category.objects.update_or_create(
                slug=slug, defaults={"name": name, "emoji": emoji, "position": pos, "parent": None})
            for sub_pos, (sub_slug, sub_name) in enumerate(subs):
                Category.objects.update_or_create(
                    slug=sub_slug, defaults={"name": sub_name, "parent": parent, "position": sub_pos})

        for slug, name, emoji, price, old, reviews, cat_slug, color in PRODUCTS:
            Product.objects.update_or_create(slug=slug, defaults={
                "name": name, "emoji": emoji, "price": price, "old_price": old,
                "reviews_count": reviews, "color": color, "is_hit": True,
                "category": Category.objects.get(slug=cat_slug),
                "description": "Тут буде опис товару: матеріал, розміри, догляд.",
            })
        self.stdout.write(self.style.SUCCESS("Готово: категорії та товари створено."))
