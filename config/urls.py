# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders.models import Order
from orders import views as order_views

original_admin_index = admin.site.index

# สร้าง Custom Admin Index ให้ส่งข้อมูล Order ที่รอตรวจสอบ
def custom_admin_index(request, extra_context=None):
    extra_context = extra_context or {}
    # ดึงเฉพาะรายการที่รอตรวจสอบสลิป (pending) มา 5 รายการล่าสุด
    extra_context['pending_orders'] = Order.objects.filter(status='pending').order_by('-created_at')[:5]
    extra_context['pending_count'] = Order.objects.filter(status='pending').count()
    
    # เรียกใช้ original_admin_index แทน admin.site.index เพื่อไม่ให้วนลูป
    return original_admin_index(request, extra_context=extra_context)

# ผูก Custom View เข้ากับ Admin Site
admin.site.index = custom_admin_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', order_views.contact_view, name='contact'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('products.urls', namespace='products')), # ให้หน้าแรกของเว็บวิ่งไปที่ App products
]

# การตั้งค่าให้ Django แสดงผลรูปภาพ media ในช่วงพัฒนาโปรเจกต์ (Debug Mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)