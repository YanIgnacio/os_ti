from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import Group

from django.http import HttpResponseForbidden

def api_user(view_func):    
    def wrap(request, *args, **kwargs):
        if  Group.objects.get(name='api_user') in request.user.groups.all() or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap

from django.http import Http404

def group_required(*groups: str):
    def decorator(function):
        def wrapper(request, *args, **kwargs):           
            qnt_verificar=len([group for group in groups])
            verificacao=[]            
            for grupo in request.user.groups.all():
                # print(grupo)
                for group in [group for group in groups]:
                    # print(group)
                    # print(group, grupo)
                    if str(group)==str(grupo):
                        verificacao.append(True)
            # print(verificacao)
            # print(qnt_verificar)
            if len(verificacao)==qnt_verificar:
                return function(request, *args, **kwargs)            
            return HttpResponseForbidden()
        return wrapper
    return decorator