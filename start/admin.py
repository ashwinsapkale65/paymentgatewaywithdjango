import imp
from django.contrib import admin
from start.models import studentpaymentremaining, studentpaymentsdone


# Register your models here.
admin.site.register(studentpaymentremaining)

admin.site.register(studentpaymentsdone)