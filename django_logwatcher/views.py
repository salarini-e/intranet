from django.shortcuts import render
from django.http import JsonResponse
from .models import ApacheAccessLog, ApacheErrorLog

def log_list_view(request):
    logs = ApacheAccessLog.objects.all().order_by('-timestamp')
    return render(request, "django_logwatcher/access_logs.html", {"logs": logs})

def log_list_json(request):
    logs = ApacheAccessLog.objects.all().order_by('-timestamp').values()
    return JsonResponse(list(logs), safe=False)

def error_log_list_view(request):
    logs = ApacheErrorLog.objects.all().order_by('-timestamp')
    return render(request, "django_logwatcher/error_logs.html", {"logs": logs})
