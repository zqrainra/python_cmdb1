from django.contrib import admin
from my_admin import UserAdmin
import models
# Register your models here.
class ServerAdmin(admin.ModelAdmin):
    fields = ('cpu_model', 'asset', 'os_type')

class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_type','asset_name','sn','manufacturer')
    filter_horizontal = ('tags',)


admin.site.register(models.Asset,AssetAdmin)
admin.site.register(models.Server,ServerAdmin)
admin.site.register(models.CPU)
admin.site.register(models.NetworkDevice)
admin.site.register(models.Software)
admin.site.register(models.Tags)
admin.site.register(models.Disk)
admin.site.register(models.RAM)
admin.site.register(models.Manufacturer)
admin.site.register(models.Business_unit)
admin.site.register(models.IDC)
admin.site.register(models.NIC)
admin.site.register(models.RaidAdaptor)
admin.site.register(models.Contract)
admin.site.register(models.EventLog)
admin.site.register(models.NewAssetApprpval)
