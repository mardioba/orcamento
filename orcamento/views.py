from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Orcamento, OrcamentoItem
from .forms import OrcamentoForm, OrcamentoItemForm
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.template.loader import render_to_string
from weasyprint import HTML

def home(request):
    return render(request, 'home.html', {})

def inserir_orcamento(request):
    if request.method == 'GET':
        form = OrcamentoForm()
        form_item_factory = inlineformset_factory(Orcamento, OrcamentoItem, form=OrcamentoItemForm, extra=2)
        form_item = form_item_factory()
        context = {
            'form': form,
            'form_item': form_item
        }
        return render(request, 'criar_orcamento.html', context)
    elif request.method == 'POST':
        form = OrcamentoForm(request.POST)
        form_item_factory = inlineformset_factory(Orcamento, OrcamentoItem, form=OrcamentoItemForm)
        form_item = form_item_factory(request.POST)
        if form.is_valid() and form_item.is_valid():
            orcamento = form.save()
            form_item.instance = orcamento
            form_item.save()
            orcamento_id = orcamento.id
            return redirect('orcamento_detail', orcamento_id)
        else:
            context = {
                'form': form,
                'form_item': form_item
            }
            return render(request, 'criar_orcamento.html', context)

def listar_orcamentos(request):
    orcamentos = Orcamento.objects.all()
    tamanho=len(orcamentos)
    if tamanho == 0:
        return render(request, 'listar_orcamentos.html', {})
    else:
        orcamentos_com_total = []
        for orcamento in orcamentos:
            total = orcamento.calcular_total()
            orcamentos_com_total.append({
                'orcamento': orcamento,
                'total': total,
            })
        context = {
            'orcamentos': orcamentos,
            'total': total
        }
        return render(request, 'listar_orcamentos.html', context)

def editar_orcamento(request, orcamento_id):
    if request.method == 'GET':
        objeto = Orcamento.objects.filter(id=orcamento_id).first()
        if objeto is None:
            return redirect('listar_orcamentos')
        form = OrcamentoForm(instance=objeto)
        form_item_factory = inlineformset_factory(Orcamento, OrcamentoItem, form=OrcamentoItemForm, extra=1)
        form_item = form_item_factory(instance=objeto)
        context = {
            'form': form,
            'form_item': form_item,
            'data': objeto.data_orcamento
        }
        return render(request, 'editar_orcamento.html', context)
    elif request.method == 'POST':
        objeto = Orcamento.objects.filter(id=orcamento_id).first()
        if objeto is None:
            return redirect('listar_orcamentos')
        form = OrcamentoForm(request.POST, instance=objeto)
        form_item_factory = inlineformset_factory(Orcamento, OrcamentoItem, form=OrcamentoItemForm)
        form_item = form_item_factory(request.POST, instance=objeto)
        if form.is_valid() and form_item.is_valid():
            orcamento = form.save()
            form_item.instance = orcamento
            form_item.save()
            return redirect('listar_orcamentos')
        else:
            context = {
                'form': form,
                'form_item': form_item,
            }
            return render(request, 'editar_orcamento.html', context)

def orcamento_detail(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)
    itens = orcamento.orcamentoitem_set.all()
    total = orcamento.calcular_total()
    return render(request, 'orcamento_detail.html', {
        'orcamento': orcamento,
        'itens': itens,
        'total': total
    })
    
class OrcamentoDeleteView(DeleteView):
    model = Orcamento
    template_name = 'orcamento_confirm_delete.html'
    success_url = reverse_lazy('listar_orcamentos')  # Redirecionar para a lista de orçamentos após a exclusão

def orcamento_pdf(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)
    itens = orcamento.orcamentoitem_set.all()
    total = orcamento.calcular_total()
    context = {
        'orcamento': orcamento,
        'itens': itens,
        'total': total
    }
    # Renderiza o template para uma string HTML
    html_string = render_to_string('orcamento_pdf.html', context)

    # Gera o PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    # Retorna o PDF como uma resposta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orcamento_{orcamento_id}.pdf"'
    return response