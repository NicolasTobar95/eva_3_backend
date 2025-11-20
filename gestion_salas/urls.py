from django.urls import path
from . import views

urlpatterns = [
    # Botones Login rapido
    path('login_admin/', views.login_admin, name='login_admin'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),

    # Vistas principales usuario/admin
    path('panel_admin/', views.panel_admin, name='panel_admin'),
    path('panel_usuario/', views.panel_usuario, name='panel_usuario'),

    # CRUD Salas (solo admin)
    path('crear_sala/', views.crear_sala, name='crear_sala'),
    path('editar_sala/<int:id>/', views.editar_sala, name='editar_sala'),
    path('eliminar_sala/<int:id>/', views.eliminar_sala, name='eliminar_sala'),
    path("detalle_sala/<int:id>/", views.detalle_sala, name="detalle_sala"),

    # Reservas (solo usuario)
    path('reservar/<int:id>/', views.reservar_sala, name='reservar_sala'),
]
