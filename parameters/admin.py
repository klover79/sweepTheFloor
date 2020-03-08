from django.contrib import admin
from .models import ActivateBoolean, EmailList, EmailType


class ActivateBooleanAdmin(admin.ModelAdmin):
    list_display = ('activation_type', 'activate')


class EmailListAdmin(admin.ModelAdmin):
    list_display = ('email_type', 'email')


admin.site.register(ActivateBoolean, ActivateBooleanAdmin)
admin.site.register(EmailList, EmailListAdmin)
admin.site.register(EmailType)
