from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.core.exceptions import ValidationError


class IdType(models.Model):
    id_type_desc = models.TextField(max_length=50)

    def __str__(self):
        return f'{self.id_type_desc} ID'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    id_type = models.ForeignKey(IdType, on_delete=models.CASCADE, blank=True, null=True)
    id_no = models.TextField(max_length=50, blank=True, null=True)
    phone_no = models.TextField(max_length=15, blank=True, null=True)
    mobile_no = models.TextField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Country(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.state}'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lot_no = models.CharField(max_length=15)
    street = models.CharField(max_length=50)
    locality = models.CharField(max_length=100, verbose_name='Locality Area or Housing/Apartment Area Name')
    postal_code = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    is_billing = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.lot_no}, {self.street}, {self.locality}, {self.postal_code}, {self.city}, {self.state}'

    def save(self, *args, **kwargs):
        if self._state.adding:  # new record action
            if Address.objects.filter(is_primary=True, user=self.user).exists() == self.is_primary:
                raise ValidationError('Record with primary address already exists.'
                                      'Please uncheck the existing primary address')
            else:
                super(Address, self).save(*args, **kwargs)
        else:  # update record action
            if not self.is_primary:
                super(Address, self).save(*args, **kwargs)
            else:  # check if is primary record already exist
                if len(Address.objects.filter(is_primary=True, user=self.user)) > 0:
                    # updating the same record with primary address
                    if self.pk == Address.objects.filter(is_primary=True, user=self.user).first().pk:
                        super(Address, self).save(*args, **kwargs)
                    else:
                        raise ValidationError('Record with primary address already exists.'
                                              'Please uncheck the existing primary address')
                else:
                    super(Address, self).save(*args, **kwargs)

