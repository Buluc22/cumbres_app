from django.contrib import admin
from .models import Alumno, Personal, Equipo, Asignacion

class SoloLecturaAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

# Register your models here.

# Registra cada modelo con el admin personalizado
admin.site.register(Alumno, SoloLecturaAdmin)
admin.site.register(Personal, SoloLecturaAdmin)
admin.site.register(Equipo, SoloLecturaAdmin)
admin.site.register(Asignacion, SoloLecturaAdmin)