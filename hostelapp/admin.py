from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User)
admin.site.register(Hostel)
admin.site.register(Hostel_verification)
admin.site.register(Complain)
admin.site.register(Payment)