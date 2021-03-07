from django.contrib import admin
from VulnManage import models
admin.site.register(models.VulnerabilityManage)
admin.site.register(models.CnvdManage)
admin.site.register(models.VulhubManage)

# Register your models here.
