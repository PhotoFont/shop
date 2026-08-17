from django.db import models

class StoreContact(models.Model):
    store_name = models.CharField(max_length=100, default="ชื่อร้านของคุณ", verbose_name="ชื่อร้าน")
    address = models.TextField(verbose_name="ที่อยู่ร้าน")
    phone = models.CharField(max_length=50, verbose_name="เบอร์โทรศัพท์")
    line_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="LINE ID", help_text="ใส่แค่ไอดี เช่น @mystore")
    facebook_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Facebook URL", help_text="ใส่ลิงก์ Facebook Page")
    
    # สำหรับเก็บโค้ด iFrame ของ Google Map
    google_map_embed = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Google Map (Embed Code)", 
        help_text="นำโค้ดฝังแผนที่ (iframe) จาก Google Maps มาวางที่นี่"
    )
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name="อัปเดตล่าสุดเมื่อ")

    class Meta:
        verbose_name = 'ตั้งค่าข้อมูลติดต่อ'
        verbose_name_plural = 'ติดต่อเรา (ตั้งค่าร้าน)'

    def __str__(self):
        return "ข้อมูลติดต่อและแผนที่ร้าน"