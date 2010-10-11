from django.contrib import admin

from models import *

admin.site.register(Product)
admin.site.register(ProductColour)
admin.site.register(ProductPhoto)
admin.site.register(TeeShirt)
admin.site.register(TeeShirtSize)
admin.site.register(Inventory)
admin.site.register(TeeShirtInventory)


