from django import template

register = template.Library()


@register.filter
def uah(value):
    """12345 → «12 345 ₴» (як toLocaleString('uk-UA') у старому script.js)."""
    try:
        return f"{int(value):,}".replace(",", "\u202f") + " ₴"
    except (TypeError, ValueError):
        return value
