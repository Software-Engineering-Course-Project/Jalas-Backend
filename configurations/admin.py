from django.contrib import admin

# Register your models here.
from configurations.models import Configuration

admin.site.register(Configuration)