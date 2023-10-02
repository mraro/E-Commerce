from django.contrib import admin

from authors.models import Profile


# Register your models here.
@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['cart']  # this an example way, can parse values from list, tuple or args
    list_display_links = 'cart',
    list_filter = 'cart',
    # search_fields = 'id', 'title', 'description', 'slug',
    # list_per_page = 20
    # list_editable = 'is_available',
    # ordering = '-id',
    # prepopulated_fields = {
    #     "slug": ('title',)  # this copy title and make a slug text in slug field
    # }
    # autocomplete_fields = 'tags',