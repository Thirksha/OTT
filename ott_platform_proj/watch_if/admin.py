from django.contrib import admin
from .models import Category, Subcategory, Movies, Tv_shows, Season, Episode, Kids
# Register your models here.


# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Movies)
admin.site.register(Tv_shows)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Kids)