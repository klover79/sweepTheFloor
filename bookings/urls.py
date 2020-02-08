from django.contrib import admin
from django.urls import path
from . import views
from .views import (BookingCreateView,
                    UserBookingListView,
                    BookingDetailView,
                    BookingUpdateView,
                    BookingDeleteView,
                    BookingAdminUpdateView)
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/admin_list', views.booking_admin_index, name='booking-admin-index'),
    path('booking/admin/<int:pk>/update', staff_member_required(BookingAdminUpdateView.as_view()),
         name='booking-admin-update'),
    path('booking/index', views.index, name='booking-index'),
    path('booking/new', BookingCreateView.as_view(), name='user-booking'),
    path('booking/<str:username>', UserBookingListView.as_view(), name='user-bookings'),
    path('booking/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('booking/<int:pk>/update', BookingUpdateView.as_view(), name='booking-update'),
    path('booking/<int:pk>/delete', BookingDeleteView.as_view(), name='booking-delete'),

    # path('about/', views.about, name='blog-about'),
]
