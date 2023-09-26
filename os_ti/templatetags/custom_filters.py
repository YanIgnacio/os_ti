from django import template
from datetime import date
import locale
from ..models import OS_Linha_Tempo, OrdemDeServico
register = template.Library()

# Função para obter o nome do mês por extenso em português
@register.filter(name='mes_extenso')
def mes_extenso(value):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    return value.strftime('%d de %B de %Y')

@register.filter(name='qntMsg')
def qntMsg(value):
    qnt_msg=OS_Linha_Tempo.objects.filter(os_id=value).count()
    status=OrdemDeServico.objects.get(id=value).message_status
    if status=='0':
        resp = str(qnt_msg) + '<i class="fa-solid fa-envelope-open ms-1"></i>'
    elif status=='1':
        resp =  str(qnt_msg) + '<i class="fa-solid fa-envelope-open-text ms-1"></i>'
    elif status=='2     ':
        resp = str(qnt_msg) + '<i class="fa-solid fa-envelope ms-1"></i>'
    else:
        resp = str(qnt_msg) + '<i class="fa-solid fa-envelope ms-1"></i>'
    return resp