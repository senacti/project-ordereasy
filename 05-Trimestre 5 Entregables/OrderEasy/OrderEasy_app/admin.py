from django.contrib import admin
from .models import Category, Product, Cliente, Pedido, PedidoItem, LoyaltyPoints, Reward, ExclusiveOffer
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Admin for Category model
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)

# Admin for Product model
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'image', 'price') 
    list_editable = ('price',)
    search_fields = ('name', 'image',)
    list_filter = ('category',)
    list_per_page = 1

# Inline for PedidoItem in PedidoAdmin
class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1

# Admin for Pedido model
class PedidoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'es_para_entrega')
    list_filter = ('estado', 'es_para_entrega', 'fecha_pedido')
    search_fields = ('cliente__user__username', 'estado')
    inlines = [PedidoItemInline]

    def save_model(self, request, obj, form, change):
        if 'estado' in form.changed_data and obj.estado == 'cancelado':
            pass
        super().save_model(request, obj, form, change)

admin.site.register(Pedido, PedidoAdmin)

# Inline for Cliente in UserAdmin
class ClienteInline(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = 'Clientes'

# Custom UserAdmin to include ClienteInline
class UserAdmin(BaseUserAdmin):
    inlines = (ClienteInline,)

# Unregister and register the User model with custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Admin for Cliente model
@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    list_display = ('user', 'direccion', 'telefono')
    search_fields = ('user__username', 'telefono')

# Admin for LoyaltyPoints model
@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(ImportExportModelAdmin):
    list_display = ('customer', 'points', 'last_updated')
    search_fields = ('customer__username',)

# Admin for Reward model
@admin.register(Reward)
class RewardAdmin(ImportExportModelAdmin):
    list_display = ('name', 'points_required', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

# Admin for ExclusiveOffer model
@admin.register(ExclusiveOffer)
class ExclusiveOfferAdmin(ImportExportModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
