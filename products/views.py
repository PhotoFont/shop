# products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    """หน้าแสดงรายการเครื่องรางทั้งหมด (มีระบบกรองตามหมวดหมู่ พร้อมสไลด์สุ่มสินค้าแนะนำ)"""
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
        
    # 🟢 สุ่มดึงวัตถุมงคลที่เปิดใช้งาน (is_active=True) มา 8 รายการสำหรับทำแถวสไลด์
    random_products = Product.objects.filter(is_active=True).order_by('?')[:8]
        
    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'random_products': random_products,  # 👈 เพิ่มตัวแปรสำหรับสไลด์สุ่มตรงนี้
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    """หน้าแสดงรายละเอียดเครื่องรางเดี่ยวๆ"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)