from django.contrib import admin

from .models import Assignment, Material, Test

admin.site.register(Material)
admin.site.register(Assignment)
admin.site.register(Test)
