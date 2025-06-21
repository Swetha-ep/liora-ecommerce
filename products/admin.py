from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Inventory)