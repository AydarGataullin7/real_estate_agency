from django.contrib import admin
from .models import Flat, Complaint, Owner


class FlatAndOwnerInline(admin.TabularInline):
    raw_id_fields = ['owner']
    model = Flat.owners.through
    verbose_name = 'Собственник'
    verbose_name_plural = 'Собственники'


class FlatAdmin(admin.ModelAdmin):
    search_fields = ('town', 'address')
    readonly_fields = ['created_at']
    list_display = ['address', 'price', 'new_building',
                    'construction_year', 'town', 'get_owner_names']
    list_editable = ['new_building']
    list_filter = ['new_building', 'rooms_number', 'has_balcony']
    raw_id_fields = ['liked_by']
    inlines = [FlatAndOwnerInline]

    def get_owner_names(self, obj):
        owners = obj.owners.all()
        return ", ".join([owner.name for owner in owners]) if owners else "Нет собственников"
    get_owner_names.short_description = 'Собственники'
    get_owner_names.admin_order_field = 'owners__name'


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complainer', 'flat', 'text', 'date']
    raw_id_fields = ['complainer', 'flat']


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phonenumber', 'pure_phone']
    raw_id_fields = ['flats']
    search_fields = ['name']


admin.site.register(Flat, FlatAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Owner, OwnerAdmin)
