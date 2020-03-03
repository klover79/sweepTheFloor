from django.db import models


class ActivateBoolean(models.Model):
    activation_type = models.CharField(unique=True, blank=False, max_length=15)
    activate = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.activation_type}'


class EmailType(models.Model):
    email_type = models.CharField(unique=True, blank=False, max_length=15)

    def __str__(self):
        return f'{self.email_type}'


class EmailList(models.Model):
    email_type = models.ForeignKey(EmailType, on_delete=models.CASCADE, max_length=15)
    email = models.EmailField(null=False)

    def __str__(self):
        return f'{self.email} | {self.email_type}'
