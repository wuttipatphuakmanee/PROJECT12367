# booking/admin.py
from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'price_per_hour')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user_name', 'start_time', 'end_time', 'booking_time')
    list_filter = ('room', 'start_time', 'booking_time')
    search_fields = ('user_name', 'room__name')
    date_hierarchy = 'start_time' # เพิ่มแถบค้นหาตามวันที่

# หรือแบบง่ายๆ ถ้าไม่ต้องการปรับแต่งมาก:
# admin.site.register(Room)
# admin.site.register(Booking)