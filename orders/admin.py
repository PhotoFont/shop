from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


# 🟢 1. Proxy Model สำหรับประวัติการขาย (แยกมาไว้นอก Class)
class SalesHistory(Order):
    class Meta:
        proxy = True
        verbose_name = 'ประวัติการขาย'
        verbose_name_plural = 'ประวัติการขาย'


# 🟢 2. Inline รายการสินค้า
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product_link', 'price', 'quantity']
    readonly_fields = ['product_link', 'price', 'quantity']
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def product_link(self, obj):
        if obj.product and getattr(obj.product, 'slug', None):
            url = f"/{obj.product.slug}/"
            return format_html(
                '<a href="{}" onclick="window.open(this.href, \'product_popup\', \'width=900,height=700,scrollbars=yes\'); return false;" '
                'style="font-weight: bold; color: #2563eb; text-decoration: underline;">'
                '🔗 {}'
                '</a>',
                url,
                obj.product.name
            )
        return obj.product.name if obj.product else "-"
    
    product_link.short_description = 'รายการวัตถุมงคล'


# 🟢 3. หน้าจัดการคำสั่งซื้อ (OrderAdmin)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'full_name', 
        'phone', 
        'line_contact',
        'tracking_number',
        'total_price', 
        'status_badge', 
        'slip_preview', 
        'created_at'
    ]
    list_editable = ['tracking_number']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'phone', 'id']
    readonly_fields = ['created_at', 'full_slip_preview']
    inlines = [OrderItemInline]
    
    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_cancelled']

    def status_badge(self, obj):
        colors = {
            'pending': 'background-color: #f59e0b; color: white;',
            'paid': 'background-color: #10b981; color: white;',
            'shipped': 'background-color: #3b82f6; color: white;',
            'cancelled': 'background-color: #ef4444; color: white;',
        }
        style = colors.get(obj.status, 'background-color: #6b7280; color: white;')
        return format_html(
            '<span style="padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 11px; {}">{}</span>',
            style,
            obj.get_status_display()
        )
    status_badge.short_description = 'สถานะ'

    def line_contact(self, obj):
        if obj.line_id:
            return format_html(
                '<a href="https://line.me/ti/p/~{}" target="_blank" style="color: #06c755; font-weight: bold;">💬 {}</a>',
                obj.line_id,
                obj.line_id
            )
        # 🟢 แก้ไข: ใช้ mark_safe แทน format_html เมื่อไม่มีการใช้ตัวแปร
        return mark_safe('<span style="color: #9ca3af;">-</span>')
    line_contact.short_description = 'LINE ID'

    def slip_preview(self, obj):
        if obj.slip_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px; border: 1px solid #d4af37;" />'
                '</a>',
                obj.slip_image.url,
                obj.slip_image.url
            )
        # 🟢 แก้ไข: ใช้ mark_safe แทน format_html เมื่อไม่มีการใช้ตัวแปร
        return mark_safe('<span style="color: #9ca3af;">ยังไม่แนบ</span>')
    slip_preview.short_description = 'สลิป'

    def full_slip_preview(self, obj):
        if obj.slip_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-width: 350px; border-radius: 8px; border: 2px solid #d4af37;" />'
                '</a>',
                obj.slip_image.url,
                obj.slip_image.url
            )
        return "ยังไม่มีการแนบสลิปโอนเงิน"
    full_slip_preview.short_description = 'รูปหลักฐานการโอนเงิน (สลิป)'

    @admin.action(description='✅ เปลี่ยนสถานะเป็น "ชำระเงินแล้ว"')
    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')

    @admin.action(description='🚚 เปลี่ยนสถานะเป็น "จัดส่งเรียบร้อย"')
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')

    @admin.action(description='❌ เปลี่ยนสถานะเป็น "ยกเลิกคำสั่งซื้อ"')
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')


# 🟢 4. หน้าจัดการประวัติการขาย (SalesHistoryAdmin)
@admin.register(SalesHistory)
class SalesHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'full_name', 'phone']
    
    # ดึง Inline ตารางรายการสินค้าเข้ามาแสดงด้านในรายละเอียดออเดอร์
    inlines = [OrderItemInline] 

    def get_queryset(self, request):
        # แสดงเฉพาะรายการขายที่ไม่อยู่ในสถานะ pending
        return super().get_queryset(request).exclude(status='pending')
