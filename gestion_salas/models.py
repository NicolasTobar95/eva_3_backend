from django.db import models
from django.utils import timezone
from datetime import timedelta

# Sala que puede ser reservada
class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad_maxima = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# Log simple usado para mostrar en pantalla las acciones
class LogAdmin(models.Model):
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.fecha.strftime('%Y-%m-%d %H:%M:%S')} - {self.mensaje}"

# Reserva de sala hecha por un usuario
class Reserva(models.Model):
    rut_reservante = models.CharField(max_length=12)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)

    fecha_hora_inicio = models.DateTimeField(default=timezone.now)
    fecha_hora_termino = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        # Asegurar máximo 2 horas
        if not self.fecha_hora_termino:
            self.fecha_hora_termino = self.fecha_hora_inicio + timedelta(hours=2)

        # Si la sala está siendo reservada -> marcar no disponible
        self.sala.disponible = False
        self.sala.save()

        super().save(*args, **kwargs)

    def liberar_sala(self):
        if timezone.now() >= self.fecha_hora_termino:
            self.sala.disponible = True
            self.sala.save()

    def __str__(self):
        return f"Reserva de {self.sala.nombre}"
