from django.urls import path, include
from orcamento.views import (inserir_orcamento, 
                             listar_orcamentos, 
                             editar_orcamento, 
                             orcamento_detail, 
                             home, 
                             OrcamentoDeleteView, 
                             orcamento_pdf, 
                             )
from django.conf import settings
from django.contrib import admin
from orcamento import views as app_views
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('criar-orcamento/', inserir_orcamento, name='criar_orcamento'),
    path('listar-orcamentos/', listar_orcamentos, name='listar_orcamentos'),
    path('editar-orcamento/<int:orcamento_id>/', editar_orcamento, name='editar_orcamento'),
    path('orcamento/<int:orcamento_id>/', orcamento_detail, name='orcamento_detail'),
    path('deletar-orcamento/<int:pk>/', OrcamentoDeleteView.as_view(), name='deletar_orcamento'),
    path('orcamento/<int:orcamento_id>/pdf/', orcamento_pdf, name='orcamento_pdf'),
    path('admin/', admin.site.urls),
    path('sair/', app_views.sair, name='sair'),
    path('accounts/', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
