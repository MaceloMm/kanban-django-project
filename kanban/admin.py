from django.contrib import admin
from .models import Task, Profile


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ('title', 'description', 'task_status', 'task_conclusion')

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('user', 'image')