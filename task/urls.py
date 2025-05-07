from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),

    path('equipos/', views.equipos_view, name='equipos'),
    path('alumnos/', views.alumnos_view, name='alumnos'),
    path('personal/', views.personal_view, name='personal'),
    path('asignacion/', views.asignacion_view, name='asignacion'),

    #Rutas CRUD de equipos
    path('equipos/agregar/', views.create_equipo, name='crear_equipo'),
    path('equipos/editar/<int:id>/', views.update_equipo, name='editar_equipo'),
    path('equipos/eliminar/<int:id>/', views.delete_equipo, name='eliminar_equipo'),

    #Rutas CRUD de alumnos
    path('alumnos/agregar/', views.create_alumno, name='crear_alumno'),
    path('alumnos/editar/<int:id_alumno>/', views.update_alumno, name='editar_alumno'),
    path('alumnos/eliminar/<int:id_alumno>/', views.delete_alumno, name='eliminar_alumno'),

    #Rutas CRUD de Personal
    path('personal/agregar/', views.create_personal, name='crear_personal'),
    path('personal/editar/<int:id>/', views.update_personal, name='editar_personal'),
    path('personal/eliminar/<int:id>/', views.delete_personal, name='eliminar_personal'),

    #Rutas CRUD de asignacion
    path('asignacion/crear/', views.create_asignacion, name='crear_asignacion'),
    path('asignacion/editar/<int:asignacion_id>/', views.update_asignacion, name='editar_asignacion'),
    path('asignacion/eliminar/<int:asignacion_id>/', views.delete_asignacion, name='eliminar_asignacion'),

]
