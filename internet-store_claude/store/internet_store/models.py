from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категорія. Два рівні: «Спальня» → «Подушки», «Ковдри», «Білизна»."""

    name = models.CharField("Назва", max_length=100)
    slug = models.SlugField("Slug (для URL)", unique=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE,
        related_name="children", verbose_name="Батьківська категорія",
    )
    emoji = models.CharField("Іконка (емодзі)", max_length=8, blank=True)
    position = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ["position", "name"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return f"{self.parent.name} → {self.name}" if self.parent else self.name

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])

    def family_ids(self):
        """id самої категорії та її підкатегорій (для відбору товарів)."""
        return [self.pk, *self.children.values_list("pk", flat=True)]


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категорія"
    )
    name = models.CharField("Назва", max_length=200)
    slug = models.SlugField("Slug (для URL)", unique=True)
    description = models.TextField("Опис", blank=True)
    price = models.PositiveIntegerField("Ціна, ₴")
    old_price = models.PositiveIntegerField("Стара ціна, ₴", null=True, blank=True,
                                            help_text="Заповніть, щоб товар потрапив у SALE")
    emoji = models.CharField("Емодзі-заглушка", max_length=8, default="🛏️",
                             help_text="Показується, поки немає фото")
    color = models.CharField("Колір фону картки", max_length=7, default="#e4e6ee")
    reviews_count = models.PositiveIntegerField("Кількість відгуків", default=0)
    is_hit = models.BooleanField("Хіт продажу", default=False)
    in_stock = models.BooleanField("В наявності", default=True)
    is_active = models.BooleanField("Показувати на сайті", default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", args=[self.slug])

    @property
    def is_sale(self):
        return bool(self.old_price and self.old_price > self.price)

    @property
    def discount_percent(self):
        return round((1 - self.price / self.old_price) * 100) if self.is_sale else 0


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новий"
        PROCESSING = "processing", "В обробці"
        SHIPPED = "shipped", "Відправлено"
        DONE = "done", "Виконано"
        CANCELED = "canceled", "Скасовано"

    class Delivery(models.TextChoices):
        NOVA = "nova", "Нова пошта"
        UKR = "ukr", "Укрпошта"
        PICKUP = "pickup", "Самовивіз (Київ)"

    class Payment(models.TextChoices):
        COD = "cod", "Післяплата"
        CARD = "card", "Картка онлайн"

    first_name = models.CharField("Ім'я", max_length=100)
    last_name = models.CharField("Прізвище", max_length=100)
    phone = models.CharField("Телефон", max_length=32)
    email = models.EmailField("Email", blank=True)
    delivery = models.CharField("Доставка", max_length=10, choices=Delivery.choices, default=Delivery.NOVA)
    city = models.CharField("Місто", max_length=100)
    address = models.CharField("Відділення / адреса", max_length=255, blank=True)
    payment = models.CharField("Оплата", max_length=10, choices=Payment.choices, default=Payment.COD)
    comment = models.TextField("Коментар", blank=True)
    status = models.CharField("Статус", max_length=12, choices=Status.choices, default=Status.NEW)
    created = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return f"Замовлення №{self.pk}"

    @property
    def total(self):
        return sum(i.subtotal for i in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name="Товар")
    name = models.CharField("Назва на момент замовлення", max_length=200)
    price = models.PositiveIntegerField("Ціна, ₴")
    quantity = models.PositiveIntegerField("Кількість", default=1)

    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"

    @property
    def subtotal(self):
        return self.price * self.quantity
