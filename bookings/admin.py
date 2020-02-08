from django.contrib import admin
from .models import BookingStatus, Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking_date', 'booking_time', 'status', 'address')


admin.site.register(BookingStatus)
admin.site.register(Booking, BookingAdmin)


