from django.urls import path
from . import views

urlpatterns = [
    path('',views.iniciogeneral, name='iniciogeneral'),
    path('index',views.index,name='index'),
    path('inicio',views.inicio,name='inicio'),

    path('Usuario/registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('Usuario/listar/', views.listar_usuarios, name='listar_usuarios'),
    path('Usuario/editarUsuario/<int:id>/', views.editarUsuario, name='editarUsuario'),
    path('procesarEdisionUsuario/', views.procesarEdisionUsuario, name='procesar_edision_usuario'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    
    path('login/', views.login_usuario, name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),

    path('Conductor/agregarConductor/',views.agregarConductor,name='agregarConductor'),
    path('Conductor/listado_conductor/',views.listado_conductor,name='listado_conductor'),
    path('Conductor/guardarConductor/', views.guardarConductor, name='guardarConductor'),
    path('Conductor/editar_conductor/<int:conductor_id>/', views.editar_conductor, name='editar_conductor'),
    path('Conductor/eliminarConductor/<int:conductor_id>/', views.eliminarConductor, name='eliminarConductor'),

    path('Bus/agregarBus/',views.agregarBus,name='agregarBus'),
    path('Bus/listado_bus/',views.listado_bus,name='listado_bus'),
    path('Bus/guardarBus/', views.guardarBus, name='guardarBus'),
    path('Bus/editar_bus/<int:bus_id>/', views.editar_bus, name='editar_bus'),
    path('Bus/eliminarBus/<int:bus_id>/', views.eliminarBus, name='eliminarBus'),

    path('Ruta/agregarRuta/',views.agregarRuta,name='agregarRuta'),
    path('Ruta/listado_ruta/',views.listado_ruta,name='listado_ruta'),
    path('Ruta/guardarRuta/', views.guardarRuta, name='guardarRuta'),
    path('Bus/editar_ruta/<int:ruta_id>/', views.editar_ruta, name='editar_ruta'),
    path('Bus/eliminarRuta/<int:ruta_id>/', views.eliminarRuta, name='eliminarRuta'),

    path('Horario/agregarHorario/',views.agregarHorario,name='agregarHorario'),
    path('Horario/listado_horario/',views.listado_horario,name='listado_horario'),
    path('Horario/listado_horariosp/',views.listado_horariosp,name='listado_horariosp'),
    path('Horario/guardarHorario/', views.guardarHorario, name='guardarHorario'),
    path('Horario/editar_horario/<int:horario_id>/', views.editar_horario, name='editar_horario'),
    path('Horario/eliminarHorario/<int:horario_id>/', views.eliminarHorario, name='eliminarHorario'),

    path('Cliente/agregarCliente/',views.agregarCliente,name='agregarCliente'),
    path('Cliente/listado_cliente/',views.listado_cliente,name='listado_cliente'),
    path('Cliente/guardarCliente/', views.guardarCliente, name='guardarCliente'),
    path('Cliente/editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('Cliente/eliminarCliente/<int:cliente_id>/', views.eliminarCliente, name='eliminarCliente'),


    path('VentaPasaje/agregarVenta/',views.agregarVenta,name='agregarVenta'),
    path('VentaPasaje/listado_venta/',views.listado_venta,name='listado_venta'),
    path('VentaPasaje/guardarVenta/', views.guardarVenta, name='guardarVenta'),
    path('VentaPasaje/editar_venta/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('VentaPasaje/eliminarVenta/<int:venta_id>/', views.eliminarVenta, name='eliminarVenta'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),

    path('VentaPasaje/factura/<int:venta_id>/', views.factura, name='factura'),
    path('dashboard_ventas/', views.dashboard_ventas, name='dashboard_ventas'),



]