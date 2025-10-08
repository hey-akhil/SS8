from django.contrib import admin
from .models import UserProfile, Address

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Group', 'CreditLimit', 'Status', 'Active']
    list_filter = ['Active', 'Group']
    search_fields = ['Name', 'Email', 'Mobile', 'Number']
    ordering = ['Name']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['AddressName', 'user', 'Address', 'City', 'State', 'Zip', 'Country', 'IsDefault']
    list_filter = ['City', 'State', 'Country', 'IsDefault']
    search_fields = ['AddressName', 'Address', 'City', 'State', 'Zip', 'Country']
    ordering = ['user', 'AddressName']
