from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.utils import timezone

# Create your views here.
def privacy_policy(request):
    privacy_policy = PrivacyPolicy.objects.first()
    context = {
        'privacy_policy': privacy_policy
    }
    return render(request, 'store/privacy-policy.html', context)


def product_list(request):
    categories = ProductCategory.objects.filter(parent=None)
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'store/product-list.html', context)


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(categoris=product.categoris).exclude(pk=pk)
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product-details.html', context)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product, created = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        print('Hello User: ', order)
        if order.products.filter(product__pk=product.pk).exists():
            cart_product.quantity +=1
            cart_product.save()
            messages.info(request, 'Quantity updated.')
            return redirect('product_details', pk=product.pk)
        else:
            order.products.add(cart_product)
            messages.success(request, 'This product add to cart.')
            return redirect('product_details', pk=product.pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
        order.products.add(cart_product)
        messages.info(request, "This product is add to cart.")
        return redirect('product_details', pk=product.pk)
    

def cart_summary(request):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'order':order,
    }
    return render(request, 'store/cart-summary.html', context)


def cart_quantity_increment(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)[0]
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            cart_product.quantity +=1
            cart_product.save()
            messages.info(request, 'Quantity updated.')
            return redirect('cart_summary')
        else:
            return redirect('cart_summary')
    else:
        return redirect('cart_summary')
    

def cart_quantity_decrement(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # product = Product.objects.get(pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            cart_product = CartProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            if cart_product.quantity > 1:
                cart_product.quantity -=1
                cart_product.save()
                messages.info(request, 'Quantity updated.')
                return redirect('cart_summary')
            else:
                cart_product.delete()
                messages.warning(request, 'Delete from cart.')
                return redirect('cart_summary')
        else:
            return redirect('cart_summary')
    else:
        return redirect('cart_summary')
    

def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            cart_product = CartProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            cart_product.delete()
            messages.warning(request, 'Delete from cart.')
            return redirect('cart_summary')
        else:
            return redirect('cart_summary')
    else:
        return redirect('cart_summary')