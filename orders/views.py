# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm, SlipUploadForm
from accounts.models import StoreContact

def order_create(request):
    """หน้ากรอกที่อยู่จัดส่งและสร้างคำสั่งซื้อ"""
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('products:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total_price()
            order.save()

            # บันทึกสินค้าแต่ละรายการ
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # ล้างตะกร้าสินค้า
            cart.clear()
            return redirect('orders:order_payment', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


def order_payment(request, order_id):
    """หน้าแสดง QR Code ชำระเงิน และแนบสลิป"""
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = SlipUploadForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders:order_success', order_id=order.id)
    else:
        form = SlipUploadForm(instance=order)

    return render(request, 'orders/payment.html', {'order': order, 'form': form})


def order_success(request, order_id):
    """หน้าแสดงความสำเร็จเมื่อแนบสลิปเรียบร้อย"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/success.html', {'order': order})

def contact_view(request):
    contact_info = StoreContact.objects.first()
    return render(request, 'contact.html', {'contact': contact_info})