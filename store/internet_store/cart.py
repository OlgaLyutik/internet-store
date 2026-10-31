from .models import Product


class Cart:
    """Кошик у сесії: {"<id товару>": кількість}."""

    KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.data = dict(self.session.get(self.KEY, {}))

    def _save(self):
        self.session[self.KEY] = self.data
        self.session.modified = True

    def add(self, product_id, qty=1):
        key = str(product_id)
        self.data[key] = min(self.data.get(key, 0) + qty, 99)
        self._save()

    def set(self, product_id, qty):
        key = str(product_id)
        if qty <= 0:
            self.data.pop(key, None)
        else:
            self.data[key] = min(qty, 99)
        self._save()

    def remove(self, product_id):
        self.data.pop(str(product_id), None)
        self._save()

    def clear(self):
        self.data = {}
        self._save()

    def __len__(self):
        return sum(self.data.values())

    def lines(self):
        products = Product.objects.filter(pk__in=self.data.keys(), is_active=True)
        return [
            {"product": p, "quantity": self.data[str(p.pk)], "subtotal": p.price * self.data[str(p.pk)]}
            for p in products
        ]

    def total(self, lines=None):
        return sum(l["subtotal"] for l in (lines if lines is not None else self.lines()))
