from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """โมเดลเก็บข้อมูลหมวดหมู่สินค้า"""
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="Slug (URL)")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="รูปหมวดหมู่")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="สร้างเมื่อ")

    class Meta:
        verbose_name = "หมวดหมู่สินค้า"
        verbose_name_plural = "ข้อมูลหมวดหมู่สินค้า"
        ordering = ['name']

    def save(self, *args, **kwargs):
        # สร้าง slug อัตโนมัติจากชื่อ หากไม่ได้กรอก
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """โมเดลเก็บข้อมูลสินค้าหลัก"""
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name="หมวดหมู่"
    )
    # name = models.CharField(max_length=200, verbose_name="ชื่อสินค้า")
    # slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug (URL)")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    def save(self, *args, **kwargs):
        # ถ้าไม่มี slug ให้สร้างอัตโนมัติจาก slugify หรือใช้ UUID หากเป็นภาษาไทย
        if not self.slug:
            slug_name = slugify(self.name)
            if not slug_name:  # กรณีชื่อเป็นภาษาไทย slugify อาจจะได้ค่าว่าง
                slug_name = f"product-{uuid.uuid4().hex[:8]}"
            self.slug = slug_name
        super().save(*args, **kwargs)
    description = models.TextField(blank=True, verbose_name="รายละเอียดสินค้า")
    
    # การจัดการราคาและส่วนลด
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคาปกติ")
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name="ราคาลดพิเศษ"
    )
    
    # การจัดการสต็อกและสถานะ
    stock = models.PositiveIntegerField(default=0, verbose_name="จำนวนในสต็อก")
    is_active = models.BooleanField(default=True, verbose_name="เปิดขายสินค้า")
    is_featured = models.BooleanField(default=False, verbose_name="สินค้าแนะนำ")
    
    # รูปภาพหลัก (Thumbnail)
    main_image = models.ImageField(upload_to='products/mains/', verbose_name="รูปภาพหลัก")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="สร้างเมื่อ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="แก้ไขล่าสุด")

    class Meta:
        verbose_name = "สินค้า"
        verbose_name_plural = "ข้อมูลสินค้า"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def get_price(self):
        """ฟังก์ชันดึงราคาขายจริง (ถ้ามีราคาลด ให้ใช้ราคาลด)"""
        if self.discount_price:
            return self.discount_price
        return self.price


class ProductImage(models.Model):
    """โมเดลเก็บรูปภาพเพิ่มเติมของสินค้า (1 สินค้า มีได้หลายรูป)"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='additional_images',
        verbose_name="สินค้า"
    )
    image = models.ImageField(upload_to='products/gallery/', verbose_name="รูปภาพประกอบ")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "รูปภาพสินค้าเพิ่มเติม"
        verbose_name_plural = "แกลเลอรีรูปภาพสินค้า"
