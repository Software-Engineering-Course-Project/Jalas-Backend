from django.contrib import admin

# Register your models here.
from logger.models import ReservationTime, Throughput

admin.site.register(ReservationTime)
admin.site.register(Throughput)