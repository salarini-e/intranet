from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required

@xframe_options_exempt
@login_required
def index(request):
    return render(request, 'index.html')