from django.contrib import admin
from .models import Sala, Reserva, LogAdmin

admin.site.register(Sala)
admin.site.register(Reserva)
admin.site.register(LogAdmin)