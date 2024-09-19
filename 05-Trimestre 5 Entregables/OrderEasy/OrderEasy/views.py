from django.shortcuts import render, redirect
from OrderEasy_app.models import Pedido, Product, Cliente, PedidoItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render
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

from django.shortcuts import render, redirect


@login_required
def hacer_pedido(request):
    if request.method == 'POST':
        direccion_entrega = request.POST.get('direccion_entrega')
        productos_seleccionados = request.POST.getlist('producto')

        # Obtener el cliente asociado al usuario logueado
        cliente = Cliente.objects.get(user=request.user)

        # Crear el pedido
        pedido = Pedido.objects.create(
            cliente= cliente,  
            direccion_entrega=direccion_entrega,
            estado='pendiente',
            es_para_entrega=True
        )

        # Asociar los productos seleccionados al pedido
        for producto_id in productos_seleccionados:
            producto = Product.objects.get(id=producto_id)  
            cantidad = int(request.POST.get(f'cantidad_{producto_id}', 1))  
            PedidoItem.objects.create(  
                pedido=pedido,  
                product=producto,  
                cantidad=cantidad  
            )

        return redirect('confirmacion_pedido', pedido_id=pedido.id)

    # Cargar los productos disponibles
    menu = Product.objects.all()  # Cambia 'Product' a 'Producto'
    return render(request, 'pedido.html', {'menu': menu})


def confirmacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'confirmacion_pedido.html', {'pedido': pedido})


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.estado != 'Cancelado' and pedido.estado != 'Entregado':
        pedido.estado = 'Cancelado'
        pedido.save()

        messages.success(request, 'Tu pedido ha sido cancelado exitosamente.')
    else:
        messages.error(request, f'No se puede cancelar el pedido porque ya ha sido {pedido.estado.lower()}.')

    return redirect(reverse('pedido'))


from .forms import ClienteUserCreationForm

def registro(request):
    if request.method == 'POST':
        form = ClienteUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index') 
    else:
        form = ClienteUserCreationForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import logout
def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('login') 
    
def MenuItem(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})



def exclusive_offers_view(request):
    offers = ExclusiveOffer.objects.filter(is_active=True).order_by('-start_date')
    return render(request, 'ofertas.html', {'offers': offers})




