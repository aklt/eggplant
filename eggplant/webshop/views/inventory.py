
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from eggplant.webshop.models.inventory import Product
from eggplant.webshop.models.cart import Basket


log = logging.getLogger(__name__)


@login_required
def webshop_home(request):
    products = Product.objects.filter(stock__gt=0, enabled=True)
    basket = Basket.objects.open_for_user(request.user)
    all_items = basket.items.all()
    ctx = {
        'basket': basket,
        'basket_items': all_items,
        'products': products
    }
    return render(request, 'eggplant/webshop/webshop_home.html', ctx)
