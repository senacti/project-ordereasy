from django.db import models

#Modelo de control de inventario

class Category(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=100)
    description = models.TextField(verbose_name='Descripción')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        db_table = 'category'
        ordering = ['id']
        

from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.telefono}"

class Product(models.Model):
    name = models.CharField('Producto', max_length=100)
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Stock')
    description = models.TextField(verbose_name='Descripción')
    image = models.ImageField(verbose_name='Imagen', upload_to='products/images', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    state = models.BooleanField(verbose_name='Disponible', default=True)
    category = models.ManyToManyField(Category, verbose_name='Categoría')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'product'
        ordering = ['id']

#modelo pedidos
class Pedido(models.Model):
    ESTADO_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_camino', 'En Camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_PEDIDO, default='pendiente')
    direccion_entrega = models.CharField(max_length=255, null=True, blank=True)
    es_para_entrega = models.BooleanField(default=False)
    nombre_usuario = models.CharField(max_length=150, default='User')

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.user.username} - {self.estado}"
    
    
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.cantidad} * {self.product.name}"
    

class MenuItem(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre



#modelo beneficios clientes
from django.conf import settings


class LoyaltyPoints(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Cliente')
    points = models.PositiveIntegerField(default=0, verbose_name='Puntos')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    def __str__(self):
        return f'{self.customer.username} - {self.points} puntos'

    class Meta:
        verbose_name = 'Punto de fidelidad'
        verbose_name_plural = 'Puntos de fidelidad'
        db_table = 'loyalty_points'
        ordering = ['-last_updated']

class Reward(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    points_required = models.PositiveIntegerField(verbose_name='Puntos requeridos')
    description = models.TextField(verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Recompensa'
        verbose_name_plural = 'Recompensas'
        db_table = 'reward'
        ordering = ['points_required']

class ExclusiveOffer(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(verbose_name='Fecha de finalización')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Oferta exclusiva'
        verbose_name_plural = 'Ofertas exclusivas'
        db_table = 'exclusive_offer'
        ordering = ['-start_date']