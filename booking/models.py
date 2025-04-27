# booking/models.py
from django.db import models
from django.utils import timezone
from decimal import Decimal # <--- มี import แล้ว ถูกต้อง
from django.core.exceptions import ValidationError # <--- มี import แล้ว ถูกต้อง

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True) # ชื่อห้อง (ไม่ซ้ำกัน)
    capacity = models.PositiveIntegerField()             # ความจุ (จำนวนเต็มบวก)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2) # ราคาต่อชั่วโมง

    def __str__(self):
        return f"{self.name} (จุ {self.capacity} คน)"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings') # เชื่อมโยงไปยังห้อง
    user_name = models.CharField(max_length=100) # ชื่อผู้จอง (แบบง่ายก่อน)
    start_time = models.DateTimeField()          # วันเวลาเริ่มต้น
    end_time = models.DateTimeField()            # วันเวลาสิ้นสุด
    booking_time = models.DateTimeField(default=timezone.now) # วันเวลาที่ทำการจอง (ใส่ค่าอัตโนมัติ)

    def __str__(self):
        return f"จองห้อง {self.room.name} โดย {self.user_name} ({self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%Y-%m-%d %H:%M')})"

    # (ตัวเลือก) เพิ่ม method สำหรับตรวจสอบความถูกต้องพื้นฐาน
    def clean(self):
        # from django.core.exceptions import ValidationError # เอาออกได้ถ้า import ไว้ข้างบนแล้ว
        if self.start_time and self.end_time: # เพิ่มการเช็คว่ามีค่าก่อนเปรียบเทียบ
            if self.start_time >= self.end_time:
                raise ValidationError("เวลาสิ้นสุดต้องอยู่หลังเวลาเริ่มต้น")
        # (ขั้นสูง) เพิ่มการตรวจสอบว่าช่วงเวลานี้มีการจองห้องนี้ไปแล้วหรือยัง
        # (โค้ดส่วนนี้ยังไม่ได้เปิดใช้งาน)
        # existing_bookings = Booking.objects.filter(
        #     room=self.room,
        #     start_time__lt=self.end_time, # เริ่มก่อนเวลาสิ้นสุดของเรา
        #     end_time__gt=self.start_time   # สิ้นสุดหลังเวลาเริ่มต้นของเรา
        # ).exclude(pk=self.pk) # ไม่นับตัวเอง (กรณีแก้ไข)
        # if existing_bookings.exists():
        #     raise ValidationError("ช่วงเวลานี้สำหรับห้องนี้ถูกจองไปแล้ว")

    # (ตัวเลือก) คำนวณระยะเวลาเป็นชั่วโมง
    @property
    def duration_hours(self):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            # ตรวจสอบเผื่อกรณี duration เป็น 0 หรือติดลบ (แม้ว่า clean จะดักไว้ระดับหนึ่ง)
            if duration.total_seconds() > 0:
                return duration.total_seconds() / 3600
        return 0 # คืนค่า 0 ถ้าไม่มี start/end time หรือ duration ไม่เป็นบวก

    # คำนวณราคารวม
    @property
    def total_price(self):
        # ตรวจสอบให้แน่ใจว่ามีข้อมูลครบถ้วนก่อนคำนวณ
        if self.start_time and self.end_time and self.room and self.room.price_per_hour is not None:
           # แปลง self.duration_hours (float) ให้เป็น Decimal ก่อนคูณ
            try:
                # ใช้ str() เพื่อแปลง float เป็น string ก่อน เพื่อความแม่นยำสูงสุดในการสร้าง Decimal
                duration_decimal = Decimal(str(self.duration_hours))
                # คูณ Decimal กับ Decimal และปัดเศษ 2 ตำแหน่ง
                calculated_price = (duration_decimal * self.room.price_per_hour).quantize(Decimal('0.01'))
                return calculated_price
            except Exception as e:
                # ในกรณีที่เกิดข้อผิดพลาดที่ไม่คาดคิดระหว่างการคำนวณ (เช่น duration_hours เป็นค่าแปลกๆ)
                print(f"Error calculating total_price: {e}") # แสดง error ใน console (สำหรับ debug)
                return Decimal('0.00') # คืนค่า 0 เพื่อป้องกัน Error หน้าเว็บ
        # คืนค่า Decimal 0.00 ถ้าเงื่อนไขไม่ครบ (เช่น ยังไม่มีราคาต่อชั่วโมง)
        return Decimal('0.00')