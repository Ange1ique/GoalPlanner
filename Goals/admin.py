from django.contrib import admin
from .models import Goals, SubGoals, Activities

# Register your models here.
admin.site.register(Goals)
admin.site.register(SubGoals)
admin.site.register(Activities)
