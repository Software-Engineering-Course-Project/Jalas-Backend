from django.contrib import admin
from jalas_back.models import *
# Register your models here.

admin.site.register(Meeting)
admin.site.register(MeetingParticipant)
admin.site.register(Poll)
admin.site.register(Select)
admin.site.register(SelectUser)
admin.site.register(ReservationTime)
