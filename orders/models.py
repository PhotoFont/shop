# orders/models.py
from django.db import models
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'รอชำระเงิน / รอตรวจสอบสลิป'),
        ('paid', 'ชำระเงินแล้ว / จัดเตรียมวัตถุมงคล'),
        ('shipped', 'จัดส่งวัตถุมงคลเรียบร้อย'),
        ('cancelled', 'ยกเลิกคำสั่งซื้อ'),
    )

    # ข้อมูลผู้สั่งซื้อ & จัดส่ง
    full_name = models.CharField(max_length=200, verbose_name="ชื่อ-นามสกุล")
    phone = models.CharField(max_length=20, verbose_name="เบอร์โทรศัพท์")
    line_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="LINE ID (สำหรับรับแจ้งเลขพัสดุ)")
    address = models.TextField(verbose_name="ที่อยู่จัดส่งวัตถุมงคล")
    
    # ข้อมูลการชำระเงิน
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคารวม")
    slip_image = models.ImageField(upload_to='slips/', blank=True, null=True, verbose_name="สลิปโอนเงิน")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="สถานะ")
    tracking_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="เลขพัสดุ (Tracking No.)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สั่งซื้อ")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อ-นามสกุล")
    phone = models.CharField(max_length=20, verbose_name="เบอร์โทรศัพท์", blank=True, null=True)
    message = models.TextField(verbose_name="ข้อความ/ข้อสงสัย")
    is_read = models.BooleanField(default=False, verbose_name="อ่านแล้ว/จัดการแล้ว")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่ติดต่อ")

    class Meta:
        verbose_name = 'ติดต่อเรา'
        verbose_name_plural = 'ข้อความติดต่อเรา'
        ordering = ['-created_at']

    def __str__(self):
        return f"ข้อความจาก {self.name}"
