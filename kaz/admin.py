from django.contrib import admin

# Register your models here.
from .models import Country, Region, Hotel, Claim, Reviews, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Hotel)
admin.site.register(Claim)
admin.site.register(Reviews)
admin.site.register(News)
