from django.shortcuts import render
from .forms import *

def IndicacaoComitePSP(request):
    if request.method == 'POST':
        form = FormIndicacaoComitePSPForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FormIndicacaoComitePSPForm()
    return render(request, 'formfacil/formfacil_indicacao_comite.html', {'form': form})