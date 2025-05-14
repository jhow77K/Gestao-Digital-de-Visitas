from django.contrib import admin
from .models import Escola, Visita, Pagamento, Monitor, Usuario

admin.site.register(Escola)
admin.site.register(Visita)
admin.site.register(Pagamento)
admin.site.register(Monitor)
admin.site.register(Usuario)