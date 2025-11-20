from django import forms
from .models import Sala, Reserva

class SalaFormulario(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ["nombre", "capacidad_maxima", "disponible"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "capacidad_maxima": forms.NumberInput(attrs={"class": "form-control"}),
            "disponible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ReservaFormulario(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["rut_reservante", "fecha_hora_inicio", "fecha_hora_termino"]
        widgets = {
            "rut_reservante": forms.TextInput(attrs={"class": "form-control"}),

            "fecha_hora_inicio": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),

            "fecha_hora_termino": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
        }
