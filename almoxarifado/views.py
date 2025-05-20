from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ItemForm, EditItemForm, AlocaItemForm, RetiraItemForm
from .models import Item, HistoricoItem
from django.db.models import Q
from .decorators import required_almoxarifado

@login_required
@required_almoxarifado
def almoxarifado(request):
    query = request.GET.get('filtro', '')
    if query:
        items = Item.objects.filter(
            Q(nome__icontains=query) | Q(id__icontains=query)
        )
    else:
        items = Item.objects.all()
    return render(request, 'almoxarifado.html', { 'items': items, 'filtro': query })

@login_required
@required_almoxarifado
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            HistoricoItem.objects.create(
                item=form.instance,
                usuario=request.user.username,
                tipo='ADICAO',
                descricao="Adição de item",
                quantidade_inicial=0,
                quantidade=form.instance.quantidade_total,
                quantidade_final=form.instance.quantidade_total
            )
            return redirect('almoxarifado:almoxarifado')
        else:
            print(form.errors)
    else:
        form = ItemForm()
    return render(request, 'form_item.html', {'form': form})

@login_required
@required_almoxarifado
def item_update(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('almoxarifado:almoxarifado')
        else:
            print(form.errors)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'form_item_edit.html', {'form': form, "item": item})

@login_required
@required_almoxarifado
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('almoxarifado:almoxarifado')
    return render(request, 'confirm_delete_item.html', {'item': item})

@login_required
@required_almoxarifado
def aloca_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = AlocaItemForm(request.POST)
        if form.is_valid():
            alocacao = form.save(commit=False)
            alocacao.item = item
            alocacao.user = request.user.username
            item = item
            quantidade_inicial = item.quantidade_total
            item.quantidade_total += alocacao.quantidade
            item.save()
            alocacao.save()
            # Salva histórico
            HistoricoItem.objects.create(
                item=item,
                usuario=alocacao.user,
                data=alocacao.data,
                tipo='ALOCACAO',
                descricao=alocacao.descricao,
                quantidade_inicial=quantidade_inicial,
                quantidade=alocacao.quantidade,
                quantidade_final=item.quantidade_total
            )
            return redirect('almoxarifado:almoxarifado')
        else:
            print(form.errors)
    else:
        form = AlocaItemForm()
    return render(request, 'aloca_item.html', {'form': form})

@login_required
@required_almoxarifado
def retira_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = RetiraItemForm(request.POST)
        if form.is_valid():
            retirada = form.save(commit=False)
            retirada.item = item
            retirada.user = request.user.username
            item = item
            if item.quantidade_total < retirada.quantidade:
                form.add_error('quantidade', 'Quantidade insuficiente em estoque.')
                return render(request, 'form_item.html', {'form': form})
            
            if retirada.quantidade == 0:
                form.add_error('quantidade', 'Quantidade deve ser maior que zero.')
                return render(request, 'form_item.html', {'form': form})
            
            quantidade_inicial = item.quantidade_total
            item.quantidade_total -= retirada.quantidade
            item.save()
            retirada.save()
            # Salva histórico
            HistoricoItem.objects.create(
                item=item,
                usuario=retirada.user,
                data=retirada.data,
                tipo='RETIRADA',
                descricao=retirada.descricao,
                quantidade_inicial=quantidade_inicial,
                quantidade=retirada.quantidade,
                quantidade_final=item.quantidade_total

            )
            return redirect('almoxarifado:almoxarifado')
        else:
            print(form.errors)
    else:
        form = RetiraItemForm()
    return render(request, 'retirada_item.html', {'form': form})

@login_required
@required_almoxarifado
def historico_view(request):
    historicos = HistoricoItem.objects.all().order_by('-data')
    return render(request, 'historico.html', {'historicos': historicos})