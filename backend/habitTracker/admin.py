# Register your models here.
from django.contrib import admin
from .models import HabitTracker, Task, Goal, DailyCompletion

admin.site.register(HabitTracker)
admin.site.register(Task)
admin.site.register(Goal)
admin.site.register(DailyCompletion)
