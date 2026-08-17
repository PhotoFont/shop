# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    """ฟังก์ชันรับค่าเพื่อเพิ่มสินค้าลงตะกร้า"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """ฟังก์ชันลบสินค้าออกจากตะกร้า"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """หน้าแสดงรายการในตะกร้าสินค้า"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
