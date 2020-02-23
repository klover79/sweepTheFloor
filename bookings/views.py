from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Booking, BookingStatus
from parameters.models import ActivateBoolean, EmailList, EmailType
from users.models import Address
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from getenv import env
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from .filters import BookingFilter
from django.core.paginator import Paginator
from mails.mailing import mail_to_user_booking, mail_to_admin_booking


def home(request):
    context = {
            # 'environ': os.environ.get('EMAIL_PASS')
            'environ': env("EMAIL_USER")
    }
    return render(request, 'bookings/home.html', context=context)


def index(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    my_filter = BookingFilter(request.GET, queryset=bookings)
    bookings = my_filter.qs

    paginator = Paginator(bookings, 5)
    page = request.GET.get('page')
    bookings = paginator.get_page(page)

    context = {
        'bookings': bookings,
        'my_filter': my_filter,
    }

    return render(request, 'bookings/index.html', context)


class BookingCreateView(LoginRequiredMixin, CreateView):

    model = Booking
    fields = ['booking_date', 'booking_time', 'address']

    def get_form(self):
        form = super().get_form()
        form.fields['booking_date'].widget = DatePickerInput()
        form.fields['booking_time'].widget = TimePickerInput()
        form.fields['address'].empty_label = 'Please select address'
        user_address = Address.objects.filter(user_id=self.request.user.id)
        form.fields['address'].queryset = user_address
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = BookingStatus.objects.filter(status_desc='Open').first()
        bookings = form.save()
        # send email notification
        user = User.objects.filter(id=self.request.user.id)
        param_email_user = ActivateBoolean.objects.filter()
        booking_id = bookings.id

        is_send_user = bool(ActivateBoolean.objects.values_list('activate',
                                                                flat=True).filter(
                                                                activation_type='send_to_user_email')[0])
        is_send_admin = bool(ActivateBoolean.objects.values_list('activate',
                                                                 flat=True).filter(
                                                                 activation_type='send_to_company_email')[0])

        if is_send_user:
            mail_to_user_booking(None,  # sender : set to none as sender default setup from system
                                 None,
                                 user[0].first_name,  # recipient_name
                                 user[0].email,  # user email
                                 'Booking Creation - Sweep The Floor',  # subject
                                 booking_id,
                                 bookings.status.status_desc,
                                 'new')   # record type
        if is_send_admin:
            mail_to_admin_booking(None,  # sender_email : set to none as sender default setup from system
                                  user[0].first_name,  # recipient_name
                                  'Booking Creation - Sweep The Floor',  # subject
                                  booking_id,
                                  'new')   # record type
        return super().form_valid(form)


class UserBookingListView(ListView):
    model = Booking
    template_name = 'bookings/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'bookings'
    # paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Booking.objects.filter(user=user).order_by('-booking_date')


class BookingDetailView(DetailView):
    model = Booking

    def get_context_data(self, **kwargs):
        context = super(BookingDetailView, self).get_context_data(**kwargs)
        status = BookingStatus.objects.filter(booking=self.get_object()).first()

        if status.status_desc == "Open":
            context['modify'] = 'enabled'
        else:
            context['modify'] = 'disabled'
            context['message'] = f'Booking status is now :  {status.status_desc}. '
        return context


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['booking_date', 'booking_time', 'address']

    def get_form(self):
        form = super().get_form()
        form.fields['booking_date'].widget = DatePickerInput()
        form.fields['booking_time'].widget = TimePickerInput()
        form.fields['address'].empty_label = 'Please select address'
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        bookings = form.save()
        # send email notification
        user = User.objects.filter(id=self.request.user.id)
        booking_id = bookings.id
        is_send_user = bool(ActivateBoolean.objects.values_list('activate',
                                                                flat=True).filter(
            activation_type='send_to_user_email')[0])

        if is_send_user:
            mail_to_user_booking(None,  # sender : set to none as sender default setup from system
                                 None,
                                 user[0].first_name,  # recipient_name
                                 user[0].email,  # user email
                                 'Booking Creation - Sweep The Floor',  # subject
                                 booking_id,
                                 bookings.status.status_desc,
                                 'update')  # record type
        return super().form_valid(form)

    def test_func(self):
        booking = self.get_object()
        if self.request.user == booking.user:
            return True
        return False


class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    success_url = '/'

    def test_func(self):
        booking = self.get_object()
        if self.request.user == booking.user:
            return True
        return False

# admin area


@user_passes_test(lambda u: u.is_staff)
def booking_admin_index(request):

    bookings = Booking.objects.all().order_by('-id')
    my_filter = BookingFilter(request.GET, queryset=bookings)
    bookings = my_filter.qs

    paginator = Paginator(bookings, 5)
    page = request.GET.get('page')
    bookings = paginator.get_page(page)

    context = {
        'bookings': bookings,
        'my_filter': my_filter,
    }

    return render(request, 'bookings/index.html', context)


class BookingAdminUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'is_staff'
    model = Booking
    fields = ['booking_date', 'booking_time', 'address', 'status']
    template_name = 'bookings/booking_admin_edit.html'
    success_url = '/booking/admin_list'
    
    def get_form(self):
        form = super().get_form()
        form.fields['booking_date'].widget = DatePickerInput()
        form.fields['booking_time'].widget = TimePickerInput()
        form.fields['address'].empty_label = 'Please select address'
        form.fields['status'].empty_label = 'Please select status'
        # assign address related to user record
        booking = self.get_object()
        form.fields['address'].queryset = Address.objects.filter(user_id=booking.user)
        return form

    def form_valid(self, form):
        bookings = form.save()
        # send email notification
        user = User.objects.filter(id=bookings.user.id)  # get user of the booking record
        booking_id = bookings.id
        mail_to_user_booking(None,  # sender : set to none as sender default setup from system
                             'Admin',  # sender_name
                             user[0].first_name,  # recipient_name
                             user[0].email,  # user email
                             'Booking Status Update - Sweep The Floor',  # subject
                             booking_id,
                             bookings.status.status_desc,
                             'update')  # record type
        return super().form_valid(form)