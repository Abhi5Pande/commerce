from django.contrib import admin
from .models import Listing, Watchlist
# Register your models here.
admin.site.register(Listing)
admin.site.register(Watchlist)