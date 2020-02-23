from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .models import Address
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import generate_token
from mails.mailing import mail_to_user_activation
from django.views import View
from .models import User
from django.conf import settings


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # default to non-active
            user.is_active = False
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account {username} has been created. '
                                      f'Please check your email for account activation')

            current_site = get_current_site(request)
            email_subject = 'Sweep The Floor - Active Account'
            message_context = {
                               'user': user,
                               'recipient_name': user.username,
                               'sender': 'Admin',
                               'domain': current_site,
                               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                               'token': generate_token.make_token(user),
                                }

            mail_to_user_activation(email_subject,
                                    user.email,
                                    message_context,
                                    )

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        user_address = Address.objects.filter(user_id=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_address': user_address
    }
    return render(request, 'users/profile.html', context)


class AddressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Address
    success_url = '/profile'

    def test_func(self):
        address = self.get_object()
        if self.request.user == address.user:
            return True
        return False


class AddressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, SuccessMessageMixin):
    model = Address
    fields = ['lot_no', 'street', 'locality', 'postal_code', 'city', 'state', 'is_billing', 'is_primary']
    success_url = '/profile'
    template_name = 'users/address_update_form.html'
    success_message = 'Address updated!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(AddressUpdateView, self).form_valid(form)
        except ValidationError:
            messages.error(self.request, 'Record with Primary Address already exists.', extra_tags='danger')
        return render(self.request, template_name=self.template_name, context=self.get_context_data())

    def test_func(self):
        address = self.get_object()
        if self.request.user == address.user:
            return True
        return False


class AddressCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):

    model = Address
    fields = ['lot_no', 'street', 'locality', 'postal_code', 'city', 'state', 'is_billing', 'is_primary']
    success_url = reverse_lazy('profile')
    template_name = 'users/address_create_form.html'
    success_message = 'Address Created'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(AddressCreateView, self).form_valid(form)
        except ValidationError:
            messages.warning(self.request, 'Record with Primary Address already exists.')
        return render(self.request, template_name=self.template_name, context=self.get_context_data())


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully. You can now login into STF')
            return redirect('login')
        return render(request, 'users/account_activate_fail.html', status=401)

