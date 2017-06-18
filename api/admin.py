from django.contrib import admin
from .models import Deliveries, DeliveryTypes, Images, ChatInfo

# Register your models here.
admin.site.register(DeliveryTypes)
admin.site.register(Deliveries)
admin.site.register(Images)
admin.site.register(ChatInfo)
