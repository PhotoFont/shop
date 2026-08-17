from django.contrib import admin
from .models import StoreContact

@admin.register(StoreContact)
class StoreContactAdmin(admin.ModelAdmin):
    # ปรับแต่งให้แสดงอะไรบ้างในหน้ารวม
    list_display = ['__str__', 'phone', 'updated_at']
    
    # 🟢 1. ปิดปุ่ม "เพิ่มข้อมูล (Add)" ถ้ามีข้อมูลอยู่แล้ว 1 ชุด
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True

    # 🟢 2. ปิดปุ่ม "ลบข้อมูล (Delete)" เพื่อป้องกันการเผลอลบการตั้งค่าร้านทิ้ง
    def has_delete_permission(self, request, obj=None):
        return False