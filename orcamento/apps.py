# orcamento/apps.py

from django.apps import AppConfig

class OrcamentoConfig(AppConfig):
    name = 'orcamento'

    def ready(self):
        import orcamento.signals