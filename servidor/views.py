from django.shortcuts import render

# Create your views here.
def listar_viagens(request):
    return render(request, 'global/templates/listagem_viagens.html')