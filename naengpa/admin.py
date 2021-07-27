from django.contrib import admin
from .models import Recipe,Review
# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['need_ingredient']
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Review)

