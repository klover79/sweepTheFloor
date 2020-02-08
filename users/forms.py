from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, IdType, Address
from django.views.generic import CreateView
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.TextInput
    last_name = forms.TextInput

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(label='Select a profile picture')
    phone_no = forms.CharField(label='Phone No (House/Office)')
    mobile_no = forms.CharField(label='Mobile Number')
    id_type = forms.ModelChoiceField(queryset=IdType.objects.all(), label='Please select your ID Type', required=False)
    id_no = forms.CharField(label='ID Number', required=False)

    class Meta:
        model = Profile
        fields = ['image', 'phone_no', 'mobile_no', 'id_type', 'id_no']


class UserAddressCreateView(CreateView):
    model = Address
    fields = ['lot_no', 'street', 'locality', 'city', 'state', 'is_billing', 'is_primary']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




