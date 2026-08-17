from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """ช่วยให้สามารถอัปโหลดหลายๆ รูปพร้อมกันในหน้าจัดการสินค้าได้"""
    model = ProductImage
    extra = 3  # จำนวนช่องอัปโหลดรูปเริ่มต้น


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}  # เจน Slug อัตโนมัติขณะพิมพ์ชื่อ


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'is_active', 'is_featured', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'is_featured', 'category', 'created_at']
    list_editable = ['price', 'discount_price', 'stock', 'is_active', 'is_featured'] # แก้ไขค่าได้เลยจากหน้าตาราง
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]  # ดึงตารางอัปโหลดรูปแกลเลอรีมาแปะรวมไว้