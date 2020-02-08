import django_filters
from django_filters import DateFilter
from bootstrap_datepicker_plus import DatePickerInput

from .models import Booking


class BookingFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='booking_date', lookup_expr='gte', label='Start Date:')
    end_date = DateFilter(field_name='booking_date', lookup_expr='lte', label='End Date:')

    def __init__(self, *args, **kwargs):
        super(BookingFilter, self).__init__(*args, **kwargs)  # populates the post
        self.form.fields['start_date'].widget = DatePickerInput()
        self.form.fields['end_date'].widget = DatePickerInput()
        self.form.fields['id'].label = 'Booking ID:'
        self.form.fields['status'].label = 'Booking Status:'

    class Meta:
        model = Booking
        # fields = '__all__'
        # exclude = ['address', 'booking_time', 'booking_date']
        fields = ['id', 'status']
