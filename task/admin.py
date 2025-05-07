from django.contrib import admin
from .models import Alumno, Personal, Equipo, Asignacion

# Register your models here.

admin.site.register(Alumno)
admin.site.register(Personal)
admin.site.register(Equipo)
admin.site.register(Asignacion)