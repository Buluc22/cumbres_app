from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Equipo
from .models import Alumno
from .models import Personal
from .models import Asignacion
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import json


# Create your views here.
#def helloword(request):
#   return HttpResponse('<h1>hola mundo</h1>')

#Vista de login
@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige a la página principal después de login
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login/login.html')

@never_cache
@login_required
def index(request):
    return render(request, 'layouts/index.html')

@login_required
def user_logout(request):
    logout(request)
    request.session.flush()  # Borra la sesión completamente
    return redirect('login')

############################
#Vistas de los templates

#Vista de inventarios
@login_required
def equipos_view(request):
    return render(request, 'equipo/equipos.html')

#Vista de alumnos
@login_required
def alumnos_view(request):
    return render(request, 'alumno/alumno.html')

#Vista de personal
@login_required
def personal_view(request):
    return render(request, 'personal/personal.html')

#Vista de asignacion
@login_required
def asignacion_view(request):
    return render(request, 'asignacion/asignacion.html')

#Vista Equipos
@login_required
def equipos_view(request):
    query = request.GET.get('q')

    if query:
        equipos = Equipo.objects.filter(NumSerie__icontains=query)
    else:
        equipos = Equipo.objects.all()

    #print(equipos)  # Esto es para verificar que haya registros

    return render(request, 'equipo/equipos.html', {'equipos': equipos, 'query': query})

#CRUD EQUIPOS
# Crear equipo
@login_required
def create_equipo(request):
    if request.method == 'POST':
        num_serie = request.POST.get('NumSerie')
        id_economico = request.POST.get('id_economico', '')  # Puede estar vacío
        if num_serie:  # Validación simple
            Equipo.objects.create(NumSerie=num_serie, id_economico=id_economico)
            return redirect('equipos')  # Redirige a la lista de equipos
    return render(request, 'equipo/create_equipo.html')

# Editar equipo
@login_required
def update_equipo(request, id):
    equipo = get_object_or_404(Equipo, id_equipo=id)
    if request.method == 'POST':
        equipo.NumSerie = request.POST.get('NumSerie', equipo.NumSerie)
        equipo.id_economico = request.POST.get('id_economico', equipo.id_economico)
        equipo.save()
        return redirect('equipos')  # Redirige a la lista de equipos
    return render(request, 'equipo/update_equipo.html', {'equipo': equipo})

# Eliminar equipo
@login_required
def delete_equipo(request, id):
    equipo = get_object_or_404(Equipo, id_equipo=id)
    if request.method == 'POST':  # Confirmación antes de eliminar
        equipo.delete()
        return redirect('equipos')
    return render(request, 'equipo/delete_equipo.html', {'equipo': equipo})

#Vista Alumnos
@login_required
def alumnos_view(request):
    query = request.GET.get('a')

    if query:
        alumnos = Alumno.objects.filter(nombre__icontains=query)
    else:
        alumnos = Alumno.objects.all()

    #print(alumnos)  # Esto es para verificar que haya registros

    return render(request, 'alumno/alumno.html', {'alumnos': alumnos, 'query': query})

# Crear alumno
@login_required
def create_alumno(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        grado = request.POST['grado']
        grupo = request.POST['grupo']
        seccion = request.POST['seccion']
        
        Alumno.objects.create(
            nombre=nombre,
            grado=grado,
            grupo=grupo,
            seccion=seccion
        )
        return redirect('alumnos')  # Redirige a la lista de alumnos

    return render(request, 'alumno/create_alumno.html')

# Editar alumno
@login_required
def update_alumno(request, id_alumno):
    alumno = get_object_or_404(Alumno, id_alumno=id_alumno)

    if request.method == 'POST':
        alumno.nombre = request.POST['nombre']
        alumno.grado = request.POST['grado']
        alumno.grupo = request.POST['grupo']
        alumno.seccion = request.POST['seccion']
        alumno.save()
        return redirect('alumnos')

    return render(request, 'alumno/update_alumno.html', {'alumno': alumno})

# Eliminar alumno
@login_required
def delete_alumno(request, id_alumno):
    alumno = get_object_or_404(Alumno, id_alumno=id_alumno)

    if request.method == 'POST':
        alumno.delete()
        return redirect('alumnos')

    return render(request, 'alumno/delete_alumno.html', {'alumno': alumno})

#Vista Personal
@login_required
def personal_view(request):
    query = request.GET.get('m')

    if query:
        personal = Personal.objects.filter(nombre__icontains=query)
    else:
        personal = Personal.objects.all()

    #print(personal)  # Esto es para verificar que haya registros

    return render(request, 'personal/personal.html', {'personal': personal, 'query': query})

# Crear personal
@login_required
def create_personal(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        puesto = request.POST['puesto']
        seccion = request.POST['seccion']

        Personal.objects.create(
            nombre=nombre,
            puesto=puesto,
            seccion=seccion
        )
        return redirect('personal')  # Redirecciona a la lista de personal
    return render(request, 'personal/create_personal.html')

# Editar personal
@login_required
def update_personal(request, id):
    personal = get_object_or_404(Personal, id_personal=id)
    
    if request.method == 'POST':
        personal.nombre = request.POST['nombre']
        personal.puesto = request.POST['puesto']
        personal.seccion = request.POST['seccion']
        personal.save()
        return redirect('personal')  # Redirecciona a la lista de personal
    
    return render(request, 'personal/update_personal.html', {'personal': personal})

# Eliminar personal
@login_required
def delete_personal(request, id):
    personal = get_object_or_404(Personal, id_personal=id)
    
    if request.method == 'POST':
        personal.delete()
        return redirect('personal')  # Redirecciona a la lista de personal
    
    return render(request, 'personal/delete_personal.html', {'personal': personal})

#Vista asignacion
@login_required
def asignacion_view(request):
    query = request.GET.get("m")
    if query:
        asignaciones = Asignacion.objects.filter(
            Q(alumno__nombre__icontains=query) | Q(personal__nombre__icontains=query)
        )
    else:
        asignaciones = Asignacion.objects.all()
    return render(request, 'asignacion/asignacion.html', {'asignaciones': asignaciones, 'query': query})

# Crear Asignacion 
@login_required
def create_asignacion(request):
    equipos = Equipo.objects.all()
    alumnos = Alumno.objects.all()
    personal = Personal.objects.all()
    errors = {}

    if request.method == 'POST':
        equipo_id = request.POST.get('equipo')
        alumno_id = request.POST.get('alumno')
        personal_id = request.POST.get('personal')
        caja = bool(request.POST.get('caja'))
        case = bool(request.POST.get('case'))
        cargador = bool(request.POST.get('cargador'))
        acuerdo_firmado = bool(request.POST.get('acuerdo_firmado'))

        asignacion = Asignacion(
            equipo_id=equipo_id,
            alumno_id=alumno_id if alumno_id else None,
            personal_id=personal_id if personal_id else None,
            caja=caja,
            case=case,
            cargador=cargador,
            acuerdo_firmado=acuerdo_firmado
        )

        try:
            asignacion.full_clean()
            asignacion.save()
            return redirect('asignacion')
        except ValidationError as e:
            errors = e.message_dict

    context = {
        'equipos': equipos,
        'alumnos': alumnos,
        'personal': personal,
        'errors': errors
    }
    return render(request, 'asignacion/create_asignacion.html', context)
'''def create_asignacion(request):
    if request.method == 'POST':
        equipo_id = request.POST.get('equipo')
        alumno_id = request.POST.get('alumno')
        personal_id = request.POST.get('personal')
        caja = bool(request.POST.get('caja'))
        case = bool(request.POST.get('case'))
        cargador = bool(request.POST.get('cargador'))
        acuerdo_firmado = bool(request.POST.get('acuerdo_firmado'))

        asignacion = Asignacion(
            equipo_id=equipo_id,
            alumno_id=alumno_id if alumno_id else None,
            personal_id=personal_id if personal_id else None,
            caja=caja,
            case=case,
            cargador=cargador,
            acuerdo_firmado=acuerdo_firmado
        )
        asignacion.full_clean()  # Llama validaciones
        asignacion.save()
        return redirect('asignacion')

    context = {
        'equipos': Equipo.objects.all(),
        'alumnos': Alumno.objects.all(),
        'personal': Personal.objects.all()
    }
    return render(request, 'asignacion/create_asignacion.html', context)'''

# Actualizar Asignacion
@login_required
def update_asignacion(request, asignacion_id):
    asignacion = get_object_or_404(Asignacion, id=asignacion_id)
    equipos = Equipo.objects.all()
    alumnos = Alumno.objects.all()
    personal = Personal.objects.all()
    errors = {}

    if request.method == 'POST':
        equipo_id = request.POST.get('equipo')
        alumno_id = request.POST.get('alumno')
        personal_id = request.POST.get('personal')

        try:
            asignacion.equipo = Equipo.objects.get(id_equipo=equipo_id)
        except (Equipo.DoesNotExist, ValueError, TypeError):
            asignacion.equipo = None

        asignacion.alumno = Alumno.objects.get(id_alumno=alumno_id) if alumno_id else None
        asignacion.personal = Personal.objects.get(id_personal=personal_id) if personal_id else None

        asignacion.caja = 'caja' in request.POST
        asignacion.case = 'case' in request.POST
        asignacion.cargador = 'cargador' in request.POST
        asignacion.acuerdo_firmado = 'acuerdo_firmado' in request.POST

        try:
            asignacion.full_clean()
            asignacion.save()
            return redirect('asignacion')
        except ValidationError as e:
            errors = e.message_dict

    return render(request, 'asignacion/update_asignacion.html', {
        'asignacion': asignacion,
        'equipos': equipos,
        'alumnos': alumnos,
        'personal': personal,
        'errors': errors
    })
'''def update_asignacion(request, asignacion_id):
    asignacion = get_object_or_404(Asignacion, id=asignacion_id)
    equipos = Equipo.objects.all()
    alumnos = Alumno.objects.all()
    personal = Personal.objects.all()

    if request.method == 'POST':
        print("Formulario enviado")
        equipo_id = request.POST.get('equipo')
        alumno_id = request.POST.get('alumno')
        personal_id = request.POST.get('personal')

        try:
            asignacion.equipo = Equipo.objects.get(id_equipo=equipo_id)
        except (Equipo.DoesNotExist, ValueError, TypeError):
            asignacion.equipo = None

        asignacion.alumno = Alumno.objects.get(id_alumno=alumno_id) if alumno_id else None
        asignacion.personal = Personal.objects.get(id_personal=personal_id) if personal_id else None

        asignacion.caja = 'caja' in request.POST
        asignacion.case = 'case' in request.POST
        asignacion.cargador = 'cargador' in request.POST
        asignacion.acuerdo_firmado = 'acuerdo_firmado' in request.POST

        try:
            asignacion.full_clean()
            print("Validación exitosa")
            asignacion.save()
            print("Guardado exitoso")
            return redirect('asignacion')
        except ValidationError as e:
            print("Errores de validación:", e.message_dict)
            return render(request, 'asignacion/update_asignacion.html', {
                'asignacion': asignacion,
                'equipos': equipos,
                'alumnos': alumnos,
                'personal': personal,
                'errors': e.message_dict
            })

    return render(request, 'asignacion/update_asignacion.html', {
        'asignacion': asignacion,
        'equipos': equipos,
        'alumnos': alumnos,
        'personal': personal
    })'''

# Eliminar Asignacion
@login_required 
def delete_asignacion(request, asignacion_id):
    asignacion = get_object_or_404(Asignacion, id=asignacion_id)

    if request.method == 'POST':
        asignacion.delete()
        return redirect('asignacion')

    return render(request, 'asignacion/delete_asignacion.html', {'asignacion': asignacion})

#Generar Responsiva PDF Personal
@login_required
def generar_responsiva_personal(request, asignacion_id):
    asignacion = Asignacion.objects.get(id=asignacion_id)

    template_path = 'asignacion/responsiva_personal.html'
    context = {
        'id_equipo': asignacion.equipo.id_equipo,
        'NumSerie': asignacion.equipo.NumSerie,
        'fecha_asignacion': asignacion.fecha_asignacion.strftime('%d/%m/%Y'),
        'cargador': 'Sí' if asignacion.cargador else 'No',
        'caja': 'Sí' if asignacion.caja else 'No',
        'case': 'Sí' if asignacion.case else 'No',
        'nombre_usuario': asignacion.personal.id_personal,  # Asegúrate de tener este campo
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="responsiva_personal.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % pisa_status.err)
    return response

#Generar Responsiva PDF Alumno
@login_required
def generar_responsiva_alumno(request, asignacion_id):
    asignacion = Asignacion.objects.get(id=asignacion_id)

    template_path = 'asignacion/responsiva_alumno.html'
    context = {
        'id_equipo': asignacion.equipo.id_equipo,
        'NumSerie': asignacion.equipo.NumSerie,
        'fecha_asignacion': asignacion.fecha_asignacion.strftime("%d/%m/%Y"),
        'nombre': asignacion.alumno.nombre,
        'grado': asignacion.alumno.grado,
        'grupo': asignacion.alumno.grupo,
        'seccion': asignacion.alumno.seccion,
        'cargador': 'Sí' if asignacion.cargador else 'No',
        'caja': 'Sí' if asignacion.caja else 'No',
        'case': 'Sí' if asignacion.case else 'No',
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=responsiva_alumno_{asignacion.id}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % pisa_status.err)
    return response

#Generar Responsivas Masivas de Personal
@login_required
def responsivas_personal_pdf(request):
    asignaciones = Asignacion.objects.filter(personal__isnull=False)

    template = get_template('asignacion/responsiva_personal.html')
    html_content = ""

    for asignacion in asignaciones:
        html = template.render({
            'id_equipo': asignacion.equipo.id_equipo,
            'NumSerie': asignacion.equipo.NumSerie,
            'fecha_asignacion': asignacion.fecha_asignacion.strftime('%d/%m/%Y'),
            'cargador': "Sí" if asignacion.cargador else "No",
            'caja': "Sí" if asignacion.caja else "No",
            'case': "Sí" if asignacion.case else "No",
        })
        html_content += html + '<p style="page-break-after: always;"></p>'

    result = BytesIO()
    pisa_status = pisa.CreatePDF(src=html_content, dest=result)

    if pisa_status.err:
        return HttpResponse("Error generando PDF", status=500)

    return HttpResponse(result.getvalue(), content_type='application/pdf')

#Generar Responsivas Masivas de Alumnos
@login_required
def responsivas_alumnos_pdf(request):
    asignaciones = Asignacion.objects.filter(alumno__isnull=False)

    template = get_template('asignacion/responsiva_alumno.html')
    html_content = ""

    for asignacion in asignaciones:
        html = template.render({
            'id_equipo': asignacion.equipo.id_equipo,
            'NumSerie': asignacion.equipo.NumSerie,
            'fecha_asignacion': asignacion.fecha_asignacion.strftime('%d/%m/%Y'),
            'nombre': asignacion.alumno.nombre,
            'grado': asignacion.alumno.grado,
            'grupo': asignacion.alumno.grupo,
            'seccion': asignacion.alumno.seccion,
            'cargador': "Sí" if asignacion.cargador else "No",
            'caja': "Sí" if asignacion.caja else "No",
            'case': "Sí" if asignacion.case else "No",
        })
        html_content += html + '<p style="page-break-after: always;"></p>'

    result = BytesIO()
    pisa_status = pisa.CreatePDF(src=html_content, dest=result)

    if pisa_status.err:
        return HttpResponse("Error generando PDF", status=500)

    return HttpResponse(result.getvalue(), content_type='application/pdf')

#Tabla del INDEX
@login_required
def index(request):
    total_alumnos = Alumno.objects.count()
    total_personal = Personal.objects.count()
    total_equipos = Equipo.objects.count()
    total_asignados = Asignacion.objects.filter(equipo__isnull=False).count()
    total_no_asignados = total_equipos - total_asignados

    # Convertir los datos a JSON seguro para JavaScript
    datos_json = json.dumps({
        "personal": total_personal,
        "alumnos": total_alumnos,
        "equipos": total_equipos,
        "asignados": total_asignados,
        "noAsignados": total_no_asignados
    })

    context = {
        "total_alumnos": total_alumnos,
        "total_personal": total_personal,
        "total_equipos": total_equipos,
        "total_asignados": total_asignados,
        "total_no_asignados": total_no_asignados,
        "datos_json": datos_json
    }

    return render(request, "layouts/index.html", context)

