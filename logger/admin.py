from django.contrib import admin

# Register your models here.
from logger.models import ReservationTime, Throughput, Response

admin.site.register(ReservationTime)
admin.site.register(Throughput)
admin.site.register(Response)