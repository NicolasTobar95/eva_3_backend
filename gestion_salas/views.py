from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Sala, Reserva, LogAdmin
from .forms import SalaFormulario, ReservaFormulario

# Funcion para mostrar el tiempo restante de una sala
def formatear_tiempo_restante(td):
    total_min = int(td.total_seconds() // 60)
    horas = total_min // 60
    mins = total_min % 60
    return f"{horas}:{mins:02d} hrs"

# 1. Pantalla inicio (ingreso usuario/contraseña)
def inicio(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        clave = request.POST.get("clave")

        # login normal
        if usuario == "admin" and clave == "admin123":
            request.session["usuario"] = "admin"
            return redirect("panel_admin")

        if usuario == "user" and clave == "user123":
            request.session["usuario"] = "usuario"
            return redirect("panel_usuario")

        return render(request, "inicio.html", {"error": "Credenciales incorrectas"})

    return render(request, "inicio.html")

# 2. Login rapido (botones)
def login_admin(request):
    request.session['usuario'] = 'admin'
    return redirect('panel_admin')

def login_usuario(request):
    request.session['usuario'] = 'usuario'
    return redirect('panel_usuario')

# 3. Panel ADMIN
def panel_admin(request):
    if request.session.get('usuario') != 'admin':
        return redirect('inicio')

    salas = Sala.objects.all()
    log_admin = LogAdmin.objects.all()[:50]

    for sala in salas:
        reserva = Reserva.objects.filter(
            sala=sala,
            fecha_hora_termino__gte=timezone.now()
        ).last()

        if reserva:
            sala.disponible = False
            rest = reserva.fecha_hora_termino - timezone.now()
            sala.tiempo_restante = formatear_tiempo_restante(rest)
        else:
            sala.disponible = True
            sala.tiempo_restante = None

    return render(request, "panel_admin.html", {"salas": salas, "log_admin": log_admin})

# 4. Panel USUARIO
def panel_usuario(request):
    if request.session.get('usuario') != 'usuario':
        return redirect('inicio')

    salas = Sala.objects.all()

    for sala in salas:
        reserva = Reserva.objects.filter(
            sala=sala,
            fecha_hora_termino__gte=timezone.now()
        ).last()

        if reserva:
            sala.disponible = False
            rest = reserva.fecha_hora_termino - timezone.now()
            sala.tiempo_restante = formatear_tiempo_restante(rest)
        else:
            sala.disponible = True
            sala.tiempo_restante = None

    return render(request, "panel_usuario.html", {"salas": salas})

# 5. Crear reserva (usuario)
def reservar_sala(request, id):
    if request.session.get("usuario") != "usuario":
        return redirect("inicio")

    sala = get_object_or_404(Sala, id=id)

    if Reserva.objects.filter(sala=sala, fecha_hora_termino__gte=timezone.now()).exists():
        return redirect("panel_usuario")

    now = timezone.now()

    if request.method == "POST":
        form = ReservaFormulario(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)

            inicio = reserva.fecha_hora_inicio
            fin = reserva.fecha_hora_termino

            # Correcciones a la hora
            if inicio < now:
                inicio = now

            if fin > inicio + timedelta(hours=2):
                fin = inicio + timedelta(hours=2)

            reserva.fecha_hora_inicio = inicio
            reserva.fecha_hora_termino = fin
            reserva.sala = sala
            reserva.save()

            LogAdmin.objects.create(mensaje=f"Reservada la sala {sala.nombre}")

            return redirect("panel_usuario")
    else:
        form = ReservaFormulario(initial={
            "fecha_hora_inicio": now.strftime('%Y-%m-%dT%H:%M'),
            "fecha_hora_termino": (now + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M'),
        })

    return render(request, "salas/reservar_sala.html", {"form": form, "sala": sala})

# 6. CRUD Salas (ADMIN)
def crear_sala(request):
    if request.session.get('usuario') != 'admin':
        return redirect('inicio')

    if request.method == "POST":
        form = SalaFormulario(request.POST)
        if form.is_valid():
            nueva = form.save()
            LogAdmin.objects.create(mensaje=f"Creada la sala {nueva.nombre}")
            return redirect('panel_admin')
    else:
        form = SalaFormulario()

    return render(request, "salas/crear_sala.html", {"form": form})



def editar_sala(request, id):
    if request.session.get('usuario') != 'admin':
        return redirect('inicio')

    sala = get_object_or_404(Sala, id=id)

    reserva_activa = Reserva.objects.filter(
        sala=sala,
        fecha_hora_termino__gte=timezone.now()
    ).last()

    if "cancelar" in request.POST:
        if reserva_activa:
            reserva_activa.fecha_hora_termino = timezone.now()
            reserva_activa.save()
            LogAdmin.objects.create(mensaje=f"Reserva cancelada en {sala.nombre}")
        return redirect("panel_admin")

    if request.method == "POST":
        form = SalaFormulario(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            LogAdmin.objects.create(mensaje=f"Editada la sala {sala.nombre}")
            return redirect('panel_admin')
    else:
        form = SalaFormulario(instance=sala)

    return render(request, "salas/editar_sala.html", {
        "form": form,
        "sala": sala,
        "reserva_activa": reserva_activa
    })



def eliminar_sala(request, id):
    if request.session.get('usuario') != 'admin':
        return redirect('inicio')

    sala = get_object_or_404(Sala, id=id)

    if request.method == "POST":
        LogAdmin.objects.create(mensaje=f"Eliminada la sala {sala.nombre}")
        sala.delete()
        return redirect('panel_admin')

    return render(request, "salas/eliminar_sala.html", {"sala": sala})


def detalle_sala(request, id):
    sala = get_object_or_404(Sala, id=id)

    reserva = Reserva.objects.filter(
        sala=sala,
        fecha_hora_termino__gte=timezone.now()
    ).last()

    return render(request, "salas/detalle_sala.html", {
        "sala": sala,
        "reserva": reserva
    })