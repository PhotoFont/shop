# orders/forms.py
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'line_id', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#120C08] border border-[#D4AF37]/30 rounded p-3 text-[#F5E6C8] focus:border-[#D4AF37] outline-none',
                'placeholder': 'ชื่อ-นามสกุล ผู้รับวัตถุมงคล'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full bg-[#120C08] border border-[#D4AF37]/30 rounded p-3 text-[#F5E6C8] focus:border-[#D4AF37] outline-none',
                'placeholder': 'เบอร์โทรศัพท์ที่ติดต่อได้'
            }),
            'line_id': forms.TextInput(attrs={
                'class': 'w-full bg-[#120C08] border border-[#D4AF37]/30 rounded p-3 text-[#F5E6C8] focus:border-[#D4AF37] outline-none',
                'placeholder': 'LINE ID (ถ้ามี เพื่อรับแจ้งเลขพัสดุ)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full bg-[#120C08] border border-[#D4AF37]/30 rounded p-3 text-[#F5E6C8] focus:border-[#D4AF37] outline-none h-28',
                'placeholder': 'บ้านเลขที่ ถนน แขวง/ตำบล เขต/อำเภอ จังหวัด รหัสไปรษณีย์'
            }),
        }

class SlipUploadForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['slip_image']