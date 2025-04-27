# booking/forms.py
from django import forms
from .models import Booking, Room
from django.core.exceptions import ValidationError
from django.utils import timezone

class BookingForm(forms.ModelForm):
    # (ตัวเลือก) เพิ่ม Widget เพื่อให้เลือกวันเวลาได้ง่ายขึ้น
    start_time = forms.DateTimeField(
        label="เวลาเริ่มต้น",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'] # รูปแบบที่รับจาก input type="datetime-local"
    )
    end_time = forms.DateTimeField(
        label="เวลาสิ้นสุด",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Booking
        fields = ['user_name', 'start_time', 'end_time'] # ระบุ field ที่จะแสดงในฟอร์ม
        labels = {
            'user_name': 'ชื่อผู้จอง',
        }

    # ทำให้ form รับค่า room มาได้ (ถ้าต้องการใช้ใน validation)
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None) # ดึงค่า room ออกมา ถ้ามี
        super().__init__(*args, **kwargs)
        # ทำให้ช่องชื่อผู้จองต้องกรอก
        self.fields['user_name'].required = True

    # Validation เพิ่มเติมสำหรับ form
    def clean_end_time(self):
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                raise ValidationError("เวลาสิ้นสุดต้องอยู่หลังเวลาเริ่มต้น")
        return end_time

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time and start_time < timezone.now():
            # อาจจะย้ายการเช็คนี้ไปที่ View หรือ clean() รวมก็ได้
            # raise ValidationError("ไม่สามารถเลือกเวลาในอดีตได้")
            pass # ย้ายไปเช็คใน view เพื่อให้ feedback ที่หน้า form ดีกว่า
        return start_time

    # (ย้ายการเช็คเวลาซ้อนทับมาที่ view แล้ว)
    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_time = cleaned_data.get('start_time')
    #     end_time = cleaned_data.get('end_time')
    #     room = self.room # ใช้ room ที่ส่งเข้ามาตอนสร้าง form

    #     if room and start_time and end_time:
    #         overlapping_bookings = Booking.objects.filter(
    #             room=room,
    #             start_time__lt=end_time,
    #             end_time__gt=start_time
    #         ).exists()
    #         if overlapping_bookings:
    #             raise ValidationError(f"ห้อง {room.name} ไม่ว่างในช่วงเวลานี้", code='overlap')

    #     return cleaned_data