from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required, admin_requerido
from .models import *
from django.utils import timezone
import datetime


@login_required
def index(request):
    #
    # Obtenemos la informacion de la BD de mensajes y comentarios
    context = {
        'mensajes'      : Mensaje.objects.all(),
        'comentarios'   : Comentario.objects.all(),
    }
    return render(request, 'index.html', context)


@admin_requerido
def administrador(request):
    context = {
        'saludo'        : 'ADMINISTRADOR'
    }
    return render(request, 'admin.html', context)



@login_required
def crea_mensaje(request):
    #
    # Comenzamos proceso POST
    if request.method == 'POST':
        #
        # Comienzan validaciones
        errors= Mensaje.objects.validador_mensaje(request.POST)
        #
        # Verificamos si hay errores, si los hay, redireccionamos con error
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        #
        # Si no hay errores capturamos datos del POST
        mensaje_post        = request.POST['mensaje']
        usuario_logueado    = request.session['usuario']['id']
        #
        # Creamos el Mensaje
        mensaje = Mensaje.objects.create(
            mensaje     = mensaje_post, 
            user        = User.objects.get(id=usuario_logueado),
            date        = timezone.now()
        )
        #
        # Enviamos Mensaje Completado y redireccionamos
        messages.success(request, "Mensaje ya esta publicado en el Muro!!!")
        return redirect("/")


def Transcurridos(fecha_inicio):

    inicio      = fecha_inicio
    fin         = timezone.now()
    inicio_dt   = datetime.datetime.strptime(str(inicio), '%Y-%m-%d %H:%M:%S.%f%z')
    fin_dt      = datetime.datetime.strptime(str(fin), '%Y-%m-%d %H:%M:%S.%f%z')
    diff        = (fin_dt - inicio_dt) 
    #print(f"En Segundos: {format(diff.seconds)}") 
    return diff.seconds





@login_required
def elimina_mensaje(request, id):
    #
    # Capturamos el Mensaje
    el_mensaje      = Mensaje.objects.get(id = id)
    #
    # Obtenemos la fecha de creacion del mensaje
    fecha_mensaje   = el_mensaje.created_at
    #
    # Enviamos a la fujcion Transcurridos la fecha de creacion del mensaje y nos devuelve el dato en segundos
    # entre la fecha de creacion del mensaje y la fecha de este proceso.
    calc            = Transcurridos(fecha_mensaje)
    #print(f"TIEMPO: {calc}")
    #
    # Comienzan las validaciones: Si ya pasaron 30 minutos...
    if calc > 1800: # Calculado en Segundos (30min = 1800seg)
        messages.warning(request, "MENSAJE NO SE PUEDE ELIMINAR DESPUES DE 30 MINUTOS")
    
    else: 
        messages.success(request, "MENSAJE ELIMINADO")
        el_mensaje.delete()
    
    return redirect("/")




@login_required
def crea_comentario(request):
    
    #
    # Comenzamos proceso POST
    if request.method == 'POST':
        #
        # Comienzan validaciones
        errors= Comentario.objects.validador_comentario(request.POST)
        #
        # Verificamos si hay errores, si los hay, redireccionamos con error
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        #
        # Si no hay errores capturamos datos del POST
        el_comentario           = request.POST['comentario']
        id_mensaje              = request.POST['id_mensaje']
        el_comentario_user_id   = request.session['usuario']['id']
        
        #
        # Creamos el Comentario
        comentario = Comentario.objects.create(
            comentario  = el_comentario, 
            user        = User.objects.get(id=el_comentario_user_id),
            mensaje     = Mensaje.objects.get(id=id_mensaje),
        )
        #
        # Enviamos Mensaje Completado y redireccionamos
        messages.success(request, "Comentario agregado correctamente")
        return redirect("/")



@login_required
def elimina_comentario(request, id):
    #
    # Capturamos el Comentario
    el_comentario       = Comentario.objects.get(id = id)
    #
    # Obtenemos la fecha de creacion del comentario
    fecha_comentario    = el_comentario.created_at
    #
    # Enviamos a la funcion Transcurridos la fecha de creacion del comentario y nos devuelve el dato en segundos
    # entre la fecha de creacion del comentario y la fecha de este proceso.
    calc                = Transcurridos(fecha_comentario)
    #print(f"TIEMPO: {calc}")
    #
    # Comienzan las validaciones: Si ya pasaron 30 minutos...
    if calc > 1800: # Calculado en Segundos (30min = 1800seg)
        messages.warning(request, "COMENTARIO NO SE PUEDE ELIMINAR DESPUES DE 30 MINUTOS")
    
    else: 
        messages.success(request, "COMENTARIO ELIMINADO")
        el_comentario.delete()
    
    return redirect("/")


