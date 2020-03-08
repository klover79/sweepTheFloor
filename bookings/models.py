from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Address


class BookingStatus(models.Model):
    status_desc = models.TextField(blank=False, max_length=50)

    def __str__(self):
        return f'{self.status_desc}'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.ForeignKey(BookingStatus, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Booking'

    def get_absolute_url(self):
        return reverse('booking-detail', kwargs={'pk': self.pk})





    



