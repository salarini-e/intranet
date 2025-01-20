def obter_ip_cliente(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]  # Caso o IP seja fornecido por proxies
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip