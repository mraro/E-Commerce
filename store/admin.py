
from django.contrib import admin

# from tags.models import TAG
from .models import E_Category, E_Commerce
# from django.contrib.contenttypes.admin import GenericStackedInline


# AQUI É UMA EXTENSÃO DO localhost:8000/admin OS MODELOS ADICIONADOS AQUI PODERÃO SER GERENCIADOS DIRETAMENTE POR # noqa
# USUARIO   # noqa

class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(E_Category, CategoryAdmin)


# UMA FORMA DE REGISTRAR AS TABELAS NO ADMIN ... # noqa
@admin.register(E_Commerce)
class CommerceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'author',
                    'is_available']  # this an example way, can parse values from list, tuple or args
    list_display_links = 'id', 'title',
    list_filter = 'category', 'author', 'is_available',
    search_fields = 'id', 'title', 'description', 'slug',
    list_per_page = 20
    list_editable = 'is_available',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)  # this copy title and make a slug text in slug field
    }
    autocomplete_fields = 'tags',
