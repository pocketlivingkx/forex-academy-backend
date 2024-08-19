from django.contrib import admin

# Register your models here.
from .models import Lesson, Test, TestAttempt, Broker, BrokerInfo  # replace YourModel with the name of your model

admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(TestAttempt)
admin.site.register(Broker)
admin.site.register(BrokerInfo)
