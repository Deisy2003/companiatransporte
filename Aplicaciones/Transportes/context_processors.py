def rol_usuario(request):
    if request.user.is_authenticated and hasattr(request.user, 'perfilusuario'):
        return {'rol_usuario': request.user.perfilusuario.rol}
    return {'rol_usuario': None}
