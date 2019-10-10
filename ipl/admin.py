from django.contrib import admin

# Register your models here.
from ipl.models import Match, Delivery

admin.site.register(Match)
admin.site.register(Delivery)
