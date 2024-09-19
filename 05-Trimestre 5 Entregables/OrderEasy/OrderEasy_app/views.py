from django.shortcuts import render, redirect
from OrderEasy_app.models import Pedido, MenuItem, PedidoItem, Cliente
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Product
from OrderEasy_app.models import ExclusiveOffer


def index(request):
    return render(request,'index.html',{
        #context
    })
def admin(request):
    return redirect('admin:index')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else: 
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html',{

    })

#pedido

@login_required
def hacer_pedido(request):
    cliente = Cliente.objects.get(user=request.user)  # Obtener el cliente basado en el usuario actual

    if request.method == 'POST':
        # Recoger datos del formulario
        direccion_entrega = request.POST.get('direccion_entrega')
        es_para_entrega = request.POST.get('es_para_entrega') == 'on'  # Checkbox
        
        # Crear el pedido
        pedido = Pedido.objects.create(
            cliente=cliente,
            direccion_entrega=direccion_entrega,
            es_para_entrega=es_para_entrega
        )
        
        # Crear los items del pedido
        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        for producto_id, cantidad in zip(productos, cantidades):
            menu_item = MenuItem.objects.get(id=producto_id)
            PedidoItem.objects.create(
                pedido=pedido,
                menu_item=menu_item,
                cantidad=int(cantidad)
            )

        return redirect('confirmacion_pedido')  # Redirige a la confirmación

    menu = MenuItem.objects.filter(disponible=True)
    return render(request, 'pedido.html', {'menu': menu})

def confirmacion_pedido(request):
    return HttpResponse("¡Gracias por tu pedido!")



from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido

def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estado != 'Cancelado' and pedido.estado != 'Entregado':
        pedido.estado = 'Cancelado'
        pedido.save()
        messages.success(request, 'Tu pedido ha sido cancelado.')
    else:
        messages.error(request, 'No se puede cancelar el pedido porque ya ha sido ' + pedido.estado.lower() + '.')
    return redirect('confirmacion_pedido', pedido_id=pedido.id)


# views.py

from OrderEasy.forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear el cliente asociado al usuario
            Cliente.objects.create(
                user=user,
                telefono=form.cleaned_data.get('telefono'),
                direccion=form.cleaned_data.get('direccion')
            )
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('index')  # Redirigir a la página de inicio o donde desees
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})


def MenuItem(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})

def exclusive_offers_view(request):
    offers = ExclusiveOffer.objects.filter(is_active=True).order_by('-start_date')
    return render(request, 'ofertas.html', {'offers': offers})
