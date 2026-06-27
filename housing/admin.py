from django.contrib import admin
from django.contrib import admin
from .models import Agent, House, Subscriber


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'whatsapp_number')
    search_fields = ('name',)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
   list_display = ('title', 'price', 'location','is_available') 
   list_filter = ('location','is_available')
   search_fields = ('title', 'location')

# Add this to the very bottom:
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
