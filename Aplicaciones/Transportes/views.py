from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import JsonResponse


from django.contrib import messages

from django.contrib.auth.models import User
from .models import Conductor, PerfilUsuario, Bus, Ruta, Horario, Cliente, Venta
from decimal import Decimal
from django.http import HttpResponseForbidden


def usuario(request):
    usuario = request.user  # Obtener el usuario logueado
    return render(request, 'usuario.html', {'usuario': usuario})


def rol_requerido(roles_permitidos):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'perfilusuario') and request.user.perfilusuario.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator
#=======================================================================================================
#INICIAR SESION
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.password == password:  # Comparar con la contraseña sin encriptar
                login(request, user)
                messages.success(request, "¡Usuario Ingresado exitosamente!")
                return redirect('inicio')  # Redirigir a la lista de usuarios después de iniciar sesión
            else:
                return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos.'})


        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuario no encontrado.'})
    
    return render(request, 'login.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('login')

#=======================================================================================================
def registrar_usuario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Contraseña en texto plano
    
        rol = request.POST.get('rol', 'Usuario')  # Valor por defecto

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
            return redirect('registrar_usuario')  # Redirigir al formulario

        # Verificar si el correo electrónico ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect('registrar_usuario')  # Redirigir al formulario

        # Crear el usuario sin encriptar la contraseña
        user = User(username=username, email=email, password=password)  # Aquí no usamos create_user
        user.save()

        # Crear el perfil de usuario
        PerfilUsuario.objects.create(
            user=user,
            rol=rol
        )

        # Mensaje de éxito
        messages.success(request, "¡Usuario registrado exitosamente!")
        return redirect('login')  # Redirigir a la página de inicio de sesión

    return render(request, 'Usuario/registrar_usuario.html')
#LISTAR USUARIOS

def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'Usuario/listar_usuarios.html', {'usuarios': usuarios})
#EDITAR USUARIO
def editarUsuario(request, id):
    usuario = User.objects.get(id=id)
    return render(request, "Usuario/actualizar_usuarios.html", {'usuario': usuario})
#ACTUALIZAR USUARIO
def procesarEdisionUsuario(request):
    usuario = User.objects.get(id=request.POST["id"])
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    rol = request.POST['rol']
    
    # Verificar si el nombre de usuario ya está en uso
    if User.objects.filter(username=username).exclude(id=usuario.id).exists():
        messages.error(request, "El nombre de usuario ya está en uso. Por favor, elija otro.")
        return render(request, "Usuario/actualizar_usuarios.html", {
            'usuario': usuario, 
            'username': username, 
            'email': email, 
            'password': password,
            'rol': rol,
        })  # Vuelve a renderizar el formulario con los valores

    # Si no hay conflictos, actualizar el usuario
    usuario.username = username
    usuario.email = email
    usuario.password = password
    usuario.save()
    
    # Si el usuario tiene un perfil, actualizamos sus datos adicionales
    if hasattr(usuario, 'perfil'):

        usuario.perfil.rol = rol
        usuario.perfil.save()
    
    # Mensaje de éxito
    messages.success(request, "¡Usuario actualizado exitosamente!")
    return redirect('listar_usuarios')


#ELIMINAR USUARIO
def eliminar_usuario(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    # Mensaje de éxito
    messages.success(request, "¡Usuario eliminado exitosamente!")
    return redirect('listar_usuarios')

#=============================================================================================

# Create your views here.
def inicio(request):
    return render(request,'inicio.html')

def index(request):
    return render(request,'index.html')

def iniciogeneral(request):
    return render(request,'iniciogeneral.html')
#=============================================================================================
#CRUD CATEGORIA

def agregarConductor(request):
    conductor=Conductor.objects.all()
    return render(request,'Conductor/agregarConductor.html',{'conductor':conductor})



def guardarConductor(request):
    if request.method == 'POST':
        nombre = request.POST['txt_nombre']
        licencia = request.POST['txt_licencia']
        fecha_nacimiento = request.POST.get('txt_fecha_nacimiento')
        fecha_ingreso = request.POST.get('txt_fecha_ingreso')
        telefono = request.POST['txt_telefono']
        direccion = request.POST['txt_direccion']
        estado = request.POST['txt_estado']
        foto = request.FILES.get('txt_foto')

        # Validar si la licencia ya existe
        if Conductor.objects.filter(licencia=licencia).exists():
            # Volver a renderizar el formulario con los datos previos y el mensaje de error
            return render(request, 'Conductor/agregarConductor.html', {
                'nombre': nombre,
                'licencia': licencia,
                'fecha_nacimiento': fecha_nacimiento,
                'fecha_ingreso': fecha_ingreso,
                'telefono': telefono,
                'direccion': direccion,
                'estado': estado,
                'foto': foto,  # Pasar la foto si es necesario
                'error_licencia': "El número de licencia ya está registrado. Por favor, ingresa uno diferente."
            })

        # Crear un nuevo conductor si la licencia no está registrada
        Conductor.objects.create(
            nombre=nombre,
            licencia=licencia,
            fecha_nacimiento=fecha_nacimiento,
            fecha_ingreso=fecha_ingreso,
            telefono=telefono,
            direccion=direccion,
            estado=estado,
            foto=foto
        )

        messages.success(request, "Conductor agregado exitosamente.")
        return redirect('agregarConductor')  # Redirigir a la URL de agregar conductor después de guardar

    return render(request, 'Conductor/agregarConductor.html')


def listado_conductor(request):
    conductor=Conductor.objects.all()
    return render(request,'Conductor/listado_conductor.html',{'conductor':conductor})

def editar_conductor(request, conductor_id):
    conductor = get_object_or_404(Conductor, id=conductor_id)
    if request.method == "POST":
        return procesarEdicionConductor(request, conductor)

    return render(request, 'Conductor/editar_conductor.html', {'conductor': conductor})

def procesarEdicionConductor(request, conductor):
    # Actualizar los datos del conductor
    conductor.nombre = request.POST.get('txt_nombre')
    conductor.licencia = request.POST.get('txt_licencia')
    conductor.fecha_nacimiento = request.POST.get('txt_fecha_nacimiento')
    conductor.fecha_ingreso = request.POST.get('txt_fecha_ingreso')
    conductor.telefono = request.POST.get('txt_telefono')
    conductor.direccion = request.POST.get('txt_direccion')
    conductor.estado = request.POST.get('txt_estado')

    # Si se carga una nueva foto, actualizarla
    if 'txt_foto' in request.FILES:
        conductor.foto = request.FILES['txt_foto']

    # Guardar los cambios en el conductor
    conductor.save()

    # Mensaje de éxito
    messages.success(request, "Conductor editado exitosamente")

    # Redirigir al listado de conductores
    return redirect('listado_conductor')

def eliminarConductor(request, conductor_id):
    conductor = get_object_or_404(Conductor, id=conductor_id)
    conductor.delete()

    messages.success(request, "Conductor eliminado exitosamente")
    return redirect('listado_conductor') 

#=============================================================================================

def agregarBus(request):
    bus = Bus.objects.all()  # Obtener todos los buses (si es necesario)
    conductor = Conductor.objects.all()  # Obtener todos los conductores
    return render(request, 'Bus/agregarBus.html', {'bus': bus, 'conductor': conductor})

def listado_bus(request):
    bus=Bus.objects.all()
    return render(request,'Bus/listado_bus.html',{'bus':bus})


def guardarBus(request):
    # Si la solicitud es un POST, es porque estamos enviando el formulario
    if request.method == 'POST':
        # Creamos una instancia del formulario con los datos enviados por POST
        numero_bus = request.POST.get('numero_bus')
        numero_placa = request.POST.get('numero_placa')
        capacidad = request.POST.get('capacidad')
        conductor_id = request.POST.get('conductor')
        conductor = Conductor.objects.get(id=conductor_id)

        # Creamos un objeto de Bus
        nuevo_bus = Bus(
            numero_bus = numero_bus,
            numero_placa=numero_placa,
            capacidad=capacidad,
            conductor=conductor,
        )
        # Guardamos el nuevo bus en la base de datos
        nuevo_bus.save()

        # Mostramos un mensaje de éxito y redirigimos a la lista de buses
        messages.success(request, 'Bus agregado exitosamente.')
        return redirect('listado_bus')

    else:
        # Si es GET, creamos un formulario vacío y mostramos la plantilla
        conductor= Conductor.objects.all()
        return render(request, 'agregar_bus.html', {'conductor': conductor})
    

def editar_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    conductor = Conductor.objects.all()
    if request.method == "POST":
        return procesarEdicionBus(request, bus)
    
    return render(request, 'Bus/editar_bus.html', {'bus': bus,'conductor': conductor})

def procesarEdicionBus(request, bus):
    # Actualizar los datos del conductor
    bus.numero_placa = request.POST.get('numero_placa')
    bus.capacidad = request.POST.get('capacidad')
    bus.conductor_id = request.POST.get('conductor')
    
    bus.save()

    messages.success(request, "Bus editado exitosamente")

    # Redirigir al listado de conductores
    return redirect('listado_bus')

def eliminarBus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    bus.delete()

    messages.success(request, "Bus eliminado exitosamente")
    return redirect('listado_bus') 

#=============================================================================================



def agregarRuta(request):
    ruta = Ruta.objects.all()  
    return render(request, 'Ruta/agregarRuta.html', { 'ruta': ruta})

def listado_ruta(request):
    ruta=Ruta.objects.all()
    return render(request,'Ruta/listado_ruta.html',{'ruta':ruta})



def guardarRuta(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        origen = request.POST.get('origen')
        destino = request.POST.get('destino')

        precio = Decimal(request.POST['precio'].replace(',', '.'))


     
        # Crear y guardar la nueva ruta
        nueva_ruta = Ruta(
            origen=origen,
            destino=destino,
            precio=precio
        )
        nueva_ruta.save()

        messages.success(request, "Ruta agregada exitosamente")
        return redirect('listado_ruta')  # Redirigir al listado de rutas
    else:
        bus = Bus.objects.all()  # Obtener todos los buses
        return render(request, 'agregarRuta.html', {'bus': bus})  # Pasar los buses a la plantilla


def editar_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id)
    if request.method == "POST":
        return procesarEdicionRuta(request, ruta)
    
    return render(request, 'Ruta/editar_ruta.html', {'ruta': ruta})

def procesarEdicionRuta(request, ruta):
    # Actualizar los datos del conductor
    ruta.origen = request.POST.get('origen')
    ruta.destino = request.POST.get('destino')
    precio_str = request.POST['precio'].replace(',', '.')
    ruta.precio = Decimal(precio_str)
    ruta.save()

    messages.success(request, "Ruta editado exitosamente")

    # Redirigir al listado de conductores
    return redirect('listado_ruta')

def eliminarRuta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id)
    ruta.delete()

    messages.success(request, "Ruta eliminado exitosamente")
    return redirect('listado_ruta') 

#=============================================================================================

def agregarHorario(request):
    horario = Horario.objects.all()  
    ruta = Ruta.objects.all()  
    bus = Bus.objects.all()  
    return render(request, 'Horario/agregarHorario.html', { 'horario': horario, 'ruta': ruta, 'bus': bus})

def listado_horario(request):
    horario = Horario.objects.all()
    return render(request, 'Horario/listado_horario.html', {'horario': horario})

def listado_horariosp(request):
    horario = Horario.objects.all()
    return render(request, 'Horario/listado_horariosp.html', {'horario': horario})

def guardarHorario(request):
    if request.method == "POST":
        ruta_id = request.POST.get('ruta')
        hora_salida = request.POST.get('hora_salida')
        hora_llegada = request.POST.get('hora_llegada')


        bus_id = request.POST.get('bus')
        ruta = Ruta.objects.get(id=ruta_id)
        bus = Bus.objects.get(id=bus_id) if bus_id else None

        # Crear el horario
        nuevo_horario = Horario(
            ruta=ruta,
            hora_salida=hora_salida,
            hora_llegada=hora_llegada,
            bus=bus
        )
        nuevo_horario.save()

        messages.success(request, "Horario agregado exitosamente.")
        return redirect('listado_horario')

    else:
        ruta = Ruta.objects.all()
        return render(request, 'Horario/agregar_horario.html', {'ruta': ruta})


from django.shortcuts import get_object_or_404

def editar_horario(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)  # Obtener el horario por ID
    ruta = Ruta.objects.all()
    bus = Bus.objects.all()  

    if request.method == "POST":
        return procesarEdicionHorario(request, horario)

    # Renderizar la plantilla de edición con los datos del horario actual
    return render(request, 'Horario/editar_horario.html', {'horario': horario,'ruta': ruta, 'bus': bus})

def procesarEdicionHorario(request, horario):
    # Actualizar los datos del horario con los valores del formulario
    horario.ruta_id = request.POST.get('ruta')
    horario.hora_salida = request.POST.get('hora_salida')
    horario.hora_llegada = request.POST.get('hora_llegada')
    bus_id = request.POST.get('bus')
    horario.bus = Bus.objects.get(id=bus_id) if bus_id else None

    

    # Guardar los cambios en la base de datos
    horario.save()

    messages.success(request, "Horario editado exitosamente.")
    return redirect('listado_horario')



def eliminarHorario(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)
    horario.delete()

    messages.success(request, "Horario eliminado exitosamente")
    return redirect('listado_horario') 

#=============================================================================================

def agregarCliente(request):
    cliente = Cliente.objects.all()  
    return render(request, 'Cliente/agregarCliente.html', { 'cliente': cliente})


def listado_cliente(request):
    cliente = Cliente.objects.all()
    return render(request, 'Cliente/listado_cliente.html', {'cliente': cliente})


def guardarCliente(request):
    if request.method == "POST":
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')

        nuevo_cliente = Cliente(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            direccion=direccion
        )
        nuevo_cliente.save()
        messages.success(request, "Cliente agregado exitosamente.")
        return redirect('listado_cliente')

    return render(request, 'Cliente/agregarCliente.html')

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        cliente.cedula = request.POST.get('cedula')
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.telefono = request.POST.get('telefono')
        cliente.email = request.POST.get('email')
        cliente.direccion = request.POST.get('direccion')
        cliente.save()
        messages.success(request, "Cliente editado exitosamente.")
        return redirect('listado_cliente')

    return render(request, 'Cliente/editar_cliente.html', {'cliente': cliente})



def eliminarCliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    messages.success(request, "Cliente eliminado exitosamente.")
    return redirect('listado_cliente')

#=============================================================================================

def agregarVenta(request):
    venta = Venta.objects.all() 
    cliente = Cliente.objects.all() 
    ruta = Ruta.objects.all() 
    horario = Horario.objects.all() 
    bus = Bus.objects.all() 
     
    return render(request, 'VentaPasaje/agregarVenta.html', { 'venta': venta,'cliente': cliente,'ruta': ruta, 'horario': horario, 'bus': bus})





def listado_venta(request):
    ventas = Venta.objects.select_related('cliente', 'ruta', 'horario').all()
    return render(request, 'VentaPasaje/listado_venta.html', {'ventas': ventas})


def guardarVenta(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion', '')

        horario_id = request.POST.get('ruta')

        # Obtener los asientos seleccionados como lista
        asientos_seleccionados = request.POST.getlist('asiento')  # Lista de asientos seleccionados
        
        # Calcular la cantidad de asientos seleccionados
        cantidad_asientos = int(request.POST.get('cantidad_seleccionada', 0))  # Obtener la cantidad de asientos seleccionados desde el formulario

        # Convertir la lista de asientos en una cadena separada por comas
        asientos_combinados = ', '.join(asientos_seleccionados)

        # Obtener precio y total de la venta
        precio = Decimal(request.POST.get('precio', '0'))
        total = Decimal(request.POST.get('total_venta', '0'))

        # Buscar o crear cliente
        cliente, created = Cliente.objects.get_or_create(
            cedula=cedula,
            defaults={'nombre': nombre, 'apellido': apellido, 'telefono': telefono, 'email': email, 'direccion': direccion}
        )
        if not created:  # Si ya existe, actualizar los datos
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.telefono = telefono
            cliente.email = email
            cliente.direccion = direccion
            cliente.save()

        # Validar horario
        horario = get_object_or_404(Horario, id=horario_id)
        bus = horario.bus

        # Crear una venta con los asientos seleccionados y la cantidad de asientos
        Venta.objects.create(
            cliente=cliente,
            bus=bus,
            horario=horario,
            ruta=horario.ruta,
            asiento=asientos_combinados,  # Guardar los asientos como una cadena
            cantidad_asientos=cantidad_asientos,  # Guardar la cantidad de asientos seleccionados
            precio=precio,
            total=total
        )

        return redirect('listado_venta')  # Redirigir al listado de ventas

    return redirect('agregarVenta')

def buscar_cliente(request):
    cedula = request.GET.get('cedula', None)

    if cedula:
        try:
            # Intentamos obtener el cliente por su cédula
            cliente = Cliente.objects.get(cedula=cedula)
            data = {
                'exists': True,
                'nombre': cliente.nombre,
                'apellido': cliente.apellido,
                'telefono': cliente.telefono,
                'email': cliente.email,
                'direccion': cliente.direccion,
            }
        except Cliente.DoesNotExist:
            # Si no existe, devolvemos 'exists': False
            data = {'exists': False}
    else:
        data = {'exists': False}

    return JsonResponse(data)




def eliminarVenta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    venta.delete()
    messages.success(request, "Venta eliminada exitosamente")
    return redirect('listado_venta')



def editar_venta(request, venta_id):
    # Obtener la venta existente
    venta = get_object_or_404(Venta, id=venta_id)

    if request.method == 'POST':
        # Actualizar los datos de la venta
        cliente = Cliente.objects.get(cedula=request.POST['cedula'])

        horario = Horario.objects.get(id=request.POST['ruta'])
        ruta = horario.ruta
        asientos = request.POST.getlist('asiento')
        cantidad_asientos = len(asientos) 

        precio_str = request.POST['total_venta']

        # Actualizar la información de la venta
        venta.cliente = cliente
        venta.ruta = ruta
        venta.horario = horario
        venta.asiento = ','.join(asientos) 
        precio_str = request.POST['precio'].replace(',', '.')
        venta.cantidad_asientos = cantidad_asientos
        venta.total = Decimal(precio_str)
        venta.save()

        return redirect('listado_venta')  # Redirigir al listado de ventas

    # Precargar los datos en el formulario
    rutas = Ruta.objects.all()
    horarios = Horario.objects.all()
    capacidad = venta.horario.bus.capacidad
    rango_asientos = range(1, capacidad + 1)  # Generar el rango de asientos
    asientos_seleccionados = venta.asiento.split(',') if venta.asiento else []
    



    return render(request, 'VentaPasaje/editar_venta.html', {
        'venta': venta,
        'rutas': rutas,
        'horarios': horarios,
        'asientos_seleccionados': asientos_seleccionados,
        'rango_asientos': rango_asientos, 
    })




def factura(request, venta_id):
    # Obtener la venta con el id proporcionado
    venta = get_object_or_404(Venta, id=venta_id)
    
    # Pasar la venta a la plantilla para su visualización
    return render(request, 'VentaPasaje/factura.html', {'venta': venta})





from django.db.models import Sum, Count
from django.db.models.functions import  TruncWeek, TruncMonth

def dashboard_ventas(request):
    # Calcular estadísticas generales
    total_ventas = Venta.objects.count()  # Total de ventas
    total_ingresos = Venta.objects.aggregate(Sum('total'))['total__sum']  # Total recaudado

    # Filtro de ventas por fecha
    filtro_fecha = request.GET.get('filtro_fecha', 'diaria')  # Por defecto 'diaria'

    if filtro_fecha == 'diaria':
        ventas_por_fecha = Venta.objects.values('fecha_compra__date') \
            .annotate(ventas=Count('id'), total_recaudado=Sum('total')) \
            .order_by('-fecha_compra__date')
    elif filtro_fecha == 'semanal':
        ventas_por_fecha = Venta.objects.annotate(semana=TruncWeek('fecha_compra')) \
            .values('semana') \
            .annotate(ventas=Count('id'), total_recaudado=Sum('total')) \
            .order_by('-semana')
    elif filtro_fecha == 'mensual':
        ventas_por_fecha = Venta.objects.annotate(mes=TruncMonth('fecha_compra')) \
            .values('mes') \
            .annotate(ventas=Count('id'), total_recaudado=Sum('total')) \
            .order_by('-mes')

    context = {
        'total_ventas': total_ventas,
        'total_ingresos': total_ingresos,
        'ventas_por_fecha': ventas_por_fecha,
        'filtro_fecha': filtro_fecha,  # Para mantener el filtro seleccionado
    }

    return render(request, 'dashboard_ventas.html', context)



