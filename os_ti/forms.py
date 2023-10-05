from django import forms
from django.forms import ModelForm, ValidationError
from .models import OrdemDeServico, Funcionario_OS, OS_ext, OS_Linha_Tempo, Pessoa
from django.contrib.auth.models import Group
from django.forms import ModelChoiceField

class OS_Form(ModelForm):    
    
    class Meta:
        model = OrdemDeServico
        widgets = {
            'tipo': forms.Select(attrs={'readonly': True}),
            'secretaria': forms.Select(),
        }
        exclude = ['numero', 'dt_inclusao', 'dt_alteracao','dt_execucao', 'observacao_pontos','atendente', 'dt_conclusao', 'prioridade', 'status', 'contribuinte', 'pontos_atendidos', 'cadastrado_por', 'message_status', 'finalizado_por']


class OS_Form_Ponto(ModelForm):    
        
    class Meta:
        model = OrdemDeServico       
        widgets={
         'dt_execucao': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
         }
        fields = ['pontos_atendidos', 'observacao_pontos', 'dt_execucao']

class PessoaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nome
    
class Funcionario_Form(ModelForm):

    pessoa = PessoaChoiceField(queryset=Pessoa.objects.none(), label='Selecione uma pessoa')

    def __init__(self, *args, **kwargs):
        grupo = kwargs.pop('grupo', None) or Group.objects.get(name='os_funcionario')
        super().__init__(*args, **kwargs)
        if grupo:
            self.fields['pessoa'].queryset = Pessoa.objects.filter(user__groups=grupo)

    class Meta:
        model = Funcionario_OS
        widgets = {'tipo_os': forms.HiddenInput()}
        fields = ['pessoa', 'nivel', 'tipo_os']

class Funcionario_Form_editar(ModelForm):

    pessoa = PessoaChoiceField(queryset=Pessoa.objects.none(), label='Selecione uma pessoa')

    def __init__(self, *args, **kwargs):
        grupo = kwargs.pop('grupo', None) or Group.objects.get(name='os_funcionario')
        super().__init__(*args, **kwargs)
        if grupo:
            self.fields['pessoa'].queryset = Pessoa.objects.filter(user__groups=grupo)

    class Meta:
        model = Funcionario_OS
        widgets = {'tipo_os': forms.HiddenInput()}
        fields = ['pessoa', 'nivel', 'tipo_os']


class Equipe_Form(ModelForm):
    class Meta:
        model = OS_ext
        widgets = {
            'equipe': forms.CheckboxSelectMultiple(),
            'os': forms.HiddenInput()

        }        
        exclude=[]

class NovaMensagemForm(forms.ModelForm):
    class Meta:
        model = OS_Linha_Tempo
        fields = ['os', 'pessoa', 'mensagem', 'anexo']
        widgets = {
            'os': forms.HiddenInput(),
            'pessoa': forms.HiddenInput(),
            'mensagem': forms.Textarea(attrs={'class': 'form-control h-100', 'rows': 6}),
            'anexo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        
#acrescentado
class CadastroForm(ModelForm):
    class Meta:
        model = Pessoa
        widgets = {
            'dt_nascimento':forms.TextInput(attrs={'type':'date'}),
            'cpf':forms.TextInput(attrs={'onkeydown': 'mascara(this, icpf)','onblur':'checkCPF(this.value)'}),
            'cep':forms.TextInput(attrs={'onkeydown': 'icep(this)','onblur':'getCEP(this)'}),
            'telefone':forms.TextInput(attrs={'onkeydown':'mascara(this, itel)'}),
        }
        fields=['matricula', 'secretaria', 'nome', 'email', 'telefone', 'dt_nascimento']
        exclude = ['user']

    # def clean_cpf(self):
    #     cpf = validate_cpf(self.cleaned_data["cpf"])
    #     return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"]
        telefone = telefone.replace('(', '')
        telefone = telefone.replace(' ', '')
        telefone = telefone.replace(')', '')
        telefone = telefone.replace('-', '')
        return telefone