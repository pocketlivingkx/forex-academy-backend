from django.contrib import admin

# Register your models here.
from .models import Lesson, Test, TestAttempt  # replace YourModel with the name of your model

admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(TestAttempt)