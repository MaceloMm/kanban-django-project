from django.contrib import admin
from .models import Task


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ('title', 'description', 'task_status', 'task_conclusion')

