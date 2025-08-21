from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "address", "city", "state", "pincode")
    search_fields = ("user__username", "phone", "city", "state")
