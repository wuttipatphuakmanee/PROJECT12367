# booking/views.py
print("Loading booking views...") # คุณสามารถลบบรรทัดนี้ออกได้หลังจากทดสอบเสร็จ

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest # สำหรับ error
from .models import Room, Booking
from .forms import BookingForm
from django.utils import timezone
from django.contrib import messages # สำหรับแสดงข้อความ feedback
from django.contrib.auth.decorators import login_required

def room_list(request):
    """แสดงรายการห้องทั้งหมด"""
    rooms = Room.objects.all().order_by('name') # ดึงห้องทั้งหมด เรียงตามชื่อ
    context = {'rooms': rooms}
    return render(request, 'booking/room_list.html', context)

@login_required
def booking_view(request, room_id):
    """แสดงฟอร์มจองสำหรับห้องที่เลือก และ xử lý การจอง"""
    room = get_object_or_404(Room, pk=room_id) # ดึงห้องที่ต้องการ ถ้าไม่เจอก็ 404

    if request.method == 'POST':
        form = BookingForm(request.POST, room=room) # ส่ง room เข้าไปใน form (ถ้าจำเป็น)
        if form.is_valid():
            # ตรวจสอบความพร้อมของห้อง (เพิ่มการตรวจสอบซ้อนทับที่นี่)
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # ตรวจสอบเวลาซ้อนทับ
            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_time__lt=end_time, # การจองที่มีอยู่ เริ่มก่อนเวลาสิ้นสุดใหม่
                end_time__gt=start_time   # การจองที่มีอยู่ สิ้นสุดหลังเวลาเริ่มต้นใหม่
            ).exists() # แค่เช็คว่ามีหรือไม่

            if overlapping_bookings:
                messages.error(request, f"ขออภัย ห้อง {room.name} ไม่ว่างในช่วงเวลาที่ท่านเลือก")
                # ส่ง form กลับไปพร้อมข้อมูลเดิมและข้อความ error
                context = {'form': form, 'room': room}
                return render(request, 'booking/booking_form.html', context)
            elif start_time < timezone.now():
                 messages.error(request, "ไม่สามารถจองเวลาย้อนหลังได้")
                 context = {'form': form, 'room': room}
                 return render(request, 'booking/booking_form.html', context)
            else:
                # สร้าง object Booking แต่ยังไม่บันทึกลง DB
                booking = form.save(commit=False)
                booking.room = room # กำหนดห้องให้กับการจอง
                booking.save() # บันทึกการจองลงฐานข้อมูล
                messages.success(request, f"จองห้อง {room.name} สำเร็จ!")
                # เปลี่ยนเส้นทางไปยังหน้ายืนยันการจอง
                return redirect(reverse('booking_success', args=[booking.id]))
        else:
            # ถ้า form ไม่ valid, แสดง form เดิมพร้อม error
            messages.error(request, "ข้อมูลการจองไม่ถูกต้อง กรุณาตรวจสอบ")
            context = {'form': form, 'room': room}
            return render(request, 'booking/booking_form.html', context)

    else: # ถ้าเป็น GET request (เข้าหน้าครั้งแรก)
        form = BookingForm(room=room) # สร้างฟอร์มเปล่า
        context = {'form': form, 'room': room}
        return render(request, 'booking/booking_form.html', context)

def booking_success(request, booking_id):
    """แสดงหน้ายืนยันการจองสำเร็จ"""
    booking = get_object_or_404(Booking, pk=booking_id)
    context = {'booking': booking}
    return render(request, 'booking/booking_success.html', context)

# (ตัวเลือก) View สำหรับแสดงการจองทั้งหมด (อาจจะต้อง login ก่อนในระบบจริง)
def all_bookings(request):
    bookings = Booking.objects.all().order_by('-start_time') # เรียงตามเวลาเริ่มล่าสุดก่อน
    context = {'bookings': bookings}
    return render(request, 'booking/all_bookings.html', context)

def booking_edit(request, booking_id):
    """หน้าสำหรับแก้ไขการจองที่มีอยู่"""
    booking = get_object_or_404(Booking, pk=booking_id)
    room = booking.room # ดึงห้องที่เกี่ยวข้องกับการจองนี้

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking, room=room) # ใช้ instance=booking เพื่อบอกว่าเป็นฟอร์มแก้ไข
        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # ตรวจสอบเวลาซ้อนทับ โดย *ไม่นับ* การจองปัจจุบัน (ที่กำลังแก้ไข)
            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=booking_id).exists() # exclude(pk=booking_id) คือส่วนสำคัญ

            if overlapping_bookings:
                messages.error(request, f"ขออภัย ห้อง {room.name} ไม่ว่างในช่วงเวลาที่ท่านเลือก (มีรายการจองอื่นอยู่)")
            elif start_time < timezone.now(): # ตรวจสอบเวลาในอดีตอีกครั้ง
                 messages.error(request, "ไม่สามารถเลือกเวลาในอดีตได้")
            else:
                try:
                    form.save() # บันทึกการเปลี่ยนแปลง
                    messages.success(request, f"แก้ไขการจองสำหรับห้อง {room.name} สำเร็จ!")
                    return redirect('all_bookings') # กลับไปหน้ารายการจองทั้งหมด
                except Exception as e:
                    messages.error(request, f"เกิดข้อผิดพลาดในการบันทึก: {e}")

        # ถ้า form ไม่ valid หรือมี overlapping bookings หรือเวลาผิดพลาด ให้แสดง form เดิมพร้อม error
        context = {'form': form, 'booking': booking, 'room': room} # ส่ง booking ไปด้วย เผื่อใช้ใน template
        # ใช้ template เดิม booking_form.html ไปก่อน หรือจะสร้าง booking_edit.html ก็ได้
        return render(request, 'booking/booking_form.html', context)


    else: # ถ้าเป็น GET request (เข้าหน้าแก้ไขครั้งแรก)
        form = BookingForm(instance=booking, room=room) # สร้างฟอร์มโดยใส่ข้อมูลเดิมของ booking ลงไป
        context = {'form': form, 'booking': booking, 'room': room}
        # แนะนำให้ใช้ template เดียวกับตอนสร้าง แต่ปรับ Title ได้
        return render(request, 'booking/booking_form.html', context) # ใช้ template เดิมไปก่อน

# (ตัวเลือก) เพิ่ม View สำหรับการลบ
def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        room_name = booking.room.name # เก็บชื่อห้องไว้ก่อนลบ
        booking.delete()
        messages.success(request, f"ลบการจองห้อง {room_name} เรียบร้อยแล้ว")
        return redirect('all_bookings')
    else:
        # ถ้าเข้าด้วย GET โดยตรง อาจ redirect กลับหรือแสดงข้อผิดพลาด
        return redirect('all_bookings')