from django.contrib import admin
from .models import CustomUser,Follow
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Follow)