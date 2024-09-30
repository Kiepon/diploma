from django.contrib import admin
from . import models
from django.contrib.auth.models import User
# Register your models here.

@admin.register(models.Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'country', 'rating')
    search_fields = ('title', 'country', 'rating', 'address')
    list_filter = ('country', 'rating')


@admin.register(models.RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'hotel',
        'room_type',
        'price_with_RUB',
        'available'
    ]
    search_fields = ('price', 'available')
    list_filter = ['price', 'available']


