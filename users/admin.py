from django.contrib import admin
from .models import Profile, IdType, State, Address, Country

admin.site.register(Profile)
admin.site.register(IdType)
admin.site.register(Address)
admin.site.register(State)
admin.site.register(Country)

