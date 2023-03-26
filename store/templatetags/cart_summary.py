from django import template
from store.models import Order

register = template.Library()


@register.simple_tag
def cart_summary(user):
    if user.is_authenticated:
        order = Order.objects.get(user=user, ordered=False)
        print(order)
        context = {
        'order':order,
    }
        return context
        
    else:
        return 0