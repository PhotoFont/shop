# views.py
from django.shortcuts import render
from accounts.models import StoreContact # import Model ที่เราเพิ่งสร้าง

def contact_view(request):
    # ดึงข้อมูลตั้งค่าร้านแถวแรกสุดมาใช้งาน
    contact_info = StoreContact.objects.first() 
    return render(request, 'contact.html', {'contact': contact_info})