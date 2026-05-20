from django.contrib import admin
from django.contrib import admin
from .models import Agent, House


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'whatsapp_number')
    search_fields = ('name',)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'agent', 'is_available')
    list_filter = ('is_available', 'location')
    search_fields = ('title', 'location')
