import os

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Value, F
from django.db.models.functions import Concat
from django.shortcuts import get_list_or_404, Http404, redirect  # object é para um só elemento
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.utils import translation

from authors.models import Profile
from base_class.view_base import Base_Global_Objects
from store.models import E_Commerce, E_Category, E_Cart
from utility.paginator import make_pagination

from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

# Create your views here.

# constant (means that not be modified, but you can in .env file) it's a var global too.
RANGE_PER_PAGE = int(os.environ.get("RANGE_PER_PAGE", 6))
OBJ_PER_PAGE = int(os.environ.get("OBJ_PER_PAGE", 9))


# THIS MAKES THE SAME THING OF func home {
class ObjectListViewBase(ListView, Base_Global_Objects):
    # This is what I can overwrite
    # allow_empty = True
    # queryset = None
    model = E_Commerce  # DATABASE
    # paginate_by = None
    # paginate_orphans = 0
    context_object_name = 'goods'  # TABLE
    # paginator_class = Paginator
    # page_kwarg = "page"
    ordering = ['-id']  # ORDERBY
    template_name = 'pages/home.html'

    def get_queryset(self, *args, **kwargs):  # RETURN A QUERYSET IN THE ORDER WORDS READ DATABASE
        # AQUI O get_published EM MODELS NÃO CHEGA
        querySet = super(ObjectListViewBase, self).get_queryset()
        querySet = querySet.filter(is_available=True, )  # (FILTER),, send data to web template html
        querySet = querySet.annotate(  # GIVE MORE ONE VARIABLE INTO A LIST OF QUERYSET
            author_full_name=Concat(
                F('author__first_name'),
                Value(" "),
                F('author__last_name'),
            )
        )

        querySetLight = querySet.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ
        querySetLight = querySetLight.prefetch_related('tags', 'author__profile')  # ! THIS IMPROVES DATABASE READ TOO
        return querySetLight

    def get_context_data(self, *args, **kwargs):
        # cart = self.get_full_cart(request=self.request)  # CARRINHO
        context = super().get_context_data(*args, **kwargs)
        pages = make_pagination(self.request, context.get('goods'), RANGE_PER_PAGE, OBJ_PER_PAGE)
        category = E_Category.objects.filter(e_commerce__isnull=False, e_commerce__is_available=True).distinct()
        language = translation.get_language()
        context.update(
            {'goods': pages['goods_page'],
             'pages': pages,
             'categories': category,
             'language': language,
             'nameSite': self.store_name,
             'current_cart': self.get_full_cart(request=self.request),

             }
        )
        return context  # UPDATE CONTEXT, IN THE OTHER WORDS, CUSTOMIZE WEB TEMPLATE WITH MY PAGINATION FUNC


# } END COMMENT

class HomeView(ObjectListViewBase):
    ...


class CategoryView(ObjectListViewBase):
    template_name = 'pages/category-view.html'

    # def get(self, *args, **kwargs):
    #     raise Http404

    def get_queryset(self, *args, **kwargs):  # RETURN A QUERYSET IN THE ORDER WORDS READ DATABASE
        querySet = super(CategoryView, self).get_queryset()
        querySet = querySet.filter(category__id=self.kwargs.get('idcategory')).order_by(
            '-id')  # (FILTER) send data to web template html
        querySetLight = querySet.select_related('author', 'category').prefetch_related(
            'tags')  # ! THIS IMPROVE DATABASE READ
        get_list_or_404(querySetLight)
        return querySetLight

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data()
        goods = context.get('goods')
        pages = make_pagination(self.request, goods, RANGE_PER_PAGE, OBJ_PER_PAGE)
        context.update(
            {
                'current_cart': self.get_full_cart(request=self.request),

                'goods': pages['goods_page'],
                'pages': pages,
                'categoryTitle': f'{goods[0].category.name}',  # ISSO É PY: F'{ VARIAVEL}' RETORNA STRING
                'is_detail': False,
            }
        )
        return context


class SearchView(ObjectListViewBase):
    template_name = 'pages/search.html'

    def get_queryset(self, *args, **kwargs):
        querySet = super(SearchView, self).get_queryset()
        var_site = self.request.GET.get('q')
        if not var_site:
            raise Http404
        var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''
        querySet = querySet.filter(Q(title__contains=var_site) |
                                   Q(description__contains=var_site) |
                                   Q(category__name__contains=var_site)).order_by('-id')
        querySet = querySet.filter(is_available=True)
        querySetLight = querySet.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ

        return querySetLight

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data()
        var_site = self.request.GET.get('q')
        var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''

        pages = make_pagination(self.request, context.get('goods'), RANGE_PER_PAGE, OBJ_PER_PAGE)
        context.update(
            {
                'current_cart': self.get_full_cart(request=self.request),
                'goods': pages['goods_page'],
                'pages': pages,
                'search_done': var_site,
            }
        )
        return context


class TagView(ObjectListViewBase):
    template_name = 'pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        querySet = super(TagView, self).get_queryset()
        var_site = self.kwargs.get('slug')

        if not var_site:
            raise Http404
        # var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''
        querySet = querySet.filter(tags__slug=var_site).order_by('-id')
        querySet = querySet.filter(is_available=True)
        querySetLight = querySet.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ

        return querySetLight

    def get_context_data(self, *args, **kwargs):
        context = super(TagView, self).get_context_data()
        # var_site = self.kwargs.get('slug')

        pages = make_pagination(self.request, context.get('goods'), RANGE_PER_PAGE, OBJ_PER_PAGE)
        context.update(
            {
                'current_cart': self.get_full_cart(request=self.request),
                'goods': pages['goods_page'],
                'pages': pages,
                # 'title': var_site
            }
        )
        return context


class Goods_View(DetailView, Base_Global_Objects):
    # DETAIL VIEW WAITS PK

    model = E_Commerce
    context_object_name = 'obj'
    template_name = 'pages/goods-view.html'

    def get_context_data(self, **kwargs):
        context = super(Goods_View, self).get_context_data()

        context.update({
            'current_cart': self.get_full_cart(request=self.request),
            'is_detail': True,
            'nameSite': self.store_name,
        })
        return context


# @method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class Cart_View(TemplateView, Base_Global_Objects):
    template_name = 'pages/cart-view.html'

    def get(self, request, *args, **kwargs):

        current_cart = self.get_full_cart(request=request)

        kwargs.update({'current_cart': current_cart,
                       'nameSite': self.store_name,
                       })
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.POST.get("_method") == 'update':  # DROP DO CARRINHO
            self.update_item_cart(request)
        else:
            id_obj = request.POST.get("id-obj")
            qtd = request.POST.get("qtd")

            self.set_item_cart(request=request, id_obj=id_obj, qtd_bought=qtd)

        return redirect(reverse('store:cart'))

