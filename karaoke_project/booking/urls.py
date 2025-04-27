# booking/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'), # หน้าแรก แสดงรายการห้อง
    path('room/<int:room_id>/book/', views.booking_view, name='booking_view'), # หน้าฟอร์มจอง
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'), # หน้าจองสำเร็จ
    path('bookings/all/', views.all_bookings, name='all_bookings'), # หน้าแสดงการจองทั้งหมด
    path('booking/edit/<int:booking_id>/', views.booking_edit, name='booking_edit'), # <-- เพิ่ม path สำหรับแก้ไข
    path('booking/delete/<int:booking_id>/', views.booking_delete, name='booking_delete'), # <-- เพิ่ม path สำหรับลบ
]