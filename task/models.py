from django.db import models

# Create your models here.
#Tabla alumnos
class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    grado = models.CharField(max_length=50)
    grupo = models.CharField(max_length=50)
    seccion = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.grado}{self.grupo} ({self.seccion})"

#tabla personal
class Personal(models.Model):
    id_personal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    puesto = models.CharField(max_length=100)
    seccion = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.puesto} ({self.seccion})"
    
#tabla equipos
class Equipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    NumSerie = models.CharField(max_length=100, unique=True)
    
    # Campo nuevo (opcional)
    id_economico = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        # Mostramos el id_economico solo si existe
        id_eco = self.id_economico if self.id_economico else "Sin ID Económico"
        return f"Equipo {self.id_equipo} - Serie: {self.NumSerie} - ID Económico: {id_eco}"


#Tabla de asigancion de equipos a usuarios
class Asignacion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, blank=True, null=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, blank=True, null=True)

    # Nuevos campos de control
    caja = models.BooleanField(default=False)
    case = models.BooleanField(default=False)
    cargador = models.BooleanField(default=False)
    acuerdo_firmado = models.BooleanField(default=False)

    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        asignado_a = self.alumno.nombre if self.alumno else self.personal.nombre
        return f"Equipo {self.equipo.NumSerie} asignado a {asignado_a}"

    def clean(self):
        from django.core.exceptions import ValidationError

        # Validar que solo se asigne a alumno o personal
        if not self.alumno and not self.personal:
            raise ValidationError("Debes asignar el equipo a un Alumno o a un Personal.")
        if self.alumno and self.personal:
            raise ValidationError("Solo puedes asignar el equipo a un Alumno o a un Personal, no a ambos.")

        # Validar que el equipo no esté ya asignado (salvo si se está actualizando la misma instancia)
        ya_asignado = Asignacion.objects.filter(equipo__id_equipo=self.equipo.id_equipo).exclude(pk=self.pk).exists()
        if ya_asignado:
            raise ValidationError(f"El equipo {self.equipo.NumSerie} ya está asignado a otro usuario.")



