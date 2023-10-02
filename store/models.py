import json
from collections import defaultdict

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.urls import reverse
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

from tags.models import TAG
from authors.models import User
from utility.image_utils import resize_img


class E_Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name  # !IMPORTANT ISSO FARA COM QUE NO ADMIN DO DJANGO RETORNE O NOME DO OBJETO

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Manager(models.Manager):
    """ CAN I USE THIS IN A VIEW, IN THIS CASE TESTS IF IS PUBLISHED """

    @staticmethod
    def get_published():
        return E_Commerce.objects.filter(is_available=True).order_by('-id').annotate(
            # GIVE MORE ONE VARIABLE INTO A LIST OF QUERYSET
            author_full_name=Concat(
                F('author__first_name'),
                Value(" "),
                F('author__last_name'),
            )
        ).select_related('author', 'category').prefetch_related(
            'tags')  # THIS IMPROVE READ DATABASE (WORKS ON FOREIGN KEY) # noqa


class E_Composition(models.Model):
    name = models.CharField(max_length=65)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)

    def __str__(self):
        return self.name  # !IMPORTANT ISSO FARA COM QUE NO ADMIN DO DJANGO RETORNE O NOME DO OBJETO

    class Meta:
        verbose_name = _("Composition")
        verbose_name_plural = _("Compositions")


class E_Commerce(models.Model):  # ISSO É UMA TABELA NO DJANGO
    objects = Manager()
    title = models.CharField(max_length=65, verbose_name=_("Title"))  # IS LIKE MYSQL VARCHAR(65)
    description = models.TextField(verbose_name=_("Description"))
    slug = models.SlugField(unique=True)
    price = models.FloatField(default=1, verbose_name=_("Price"))
    quantity = models.IntegerField(default=0, verbose_name=_("Quantity"))
    # preparetion_steps = models.TextField(null=True, blank=True)
    # preparetion_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Update at"))
    is_available = models.BooleanField(default=False, verbose_name=_("Is Available"))

    composition = models.ForeignKey(
        E_Composition, on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name=_("Compositions"),
    )
    category = models.ForeignKey(
        E_Category, on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name=_("Category"),
    )  # FOREING KEY (CHAVE ESTRANGERIA COM A class Category) on_delete definira o campo como null para não perder os
    # links com demais informações
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("Author")
    )
    # GENERIC
    # tags = GenericRelation(
    #     TAG, related_query_name='Remedios'
    # )
    # MANY TO MANY
    tags = models.ManyToManyField(TAG, verbose_name="TAG", blank=True)
    # cover = models.ManyToManyField(Covers, verbose_name="Images")
    # cover = models.ImageField(upload_to='covers/%Y/%m/%d/',
    #                           verbose_name="Cover/Image")  # campo de imagem
    cover = models.TextField(blank=True, null=True)

    def get_multiview_images_list(self):
        if self.cover:
            try:
                urls = json.loads(self.cover)
                return [url for url in urls]
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
        return []

    def get_default_image(self):
        if self.cover:
            try:
                urls = json.loads(self.cover)
                return [url for url in urls][0]
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
        return [] # TODO por uma imagem default aqui

    def set_multiview_images(self, images):
        self.multiview_images = json.dumps(images)

    # (blank=True permite campo vazio, default é a imagem padrão caso não exista

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # THIS IS SO IMPORTANT, THIS IS CALLED IN TEMPLATE HTML (HAS THIS IN remedio.html)
        return reverse('store:goods', args=(self.id,))

    class Meta:
        verbose_name = _("Object")
        verbose_name_plural = _("Objects")


class Covers(models.Model):
    cover = models.ImageField(upload_to='covers/%Y/%m/%d/',
                              verbose_name="Cover/Image")  # campo de imagem
    project = models.ForeignKey(E_Commerce, on_delete=models.CASCADE)


# Carrinho
class Manage_cart(Manager):
    def set_item_cart(self, request, id_obj, qtd_bought):

        instance_obj = E_Commerce.objects.get(pk=int(id_obj))
        # se o usuario estiver logado adicione no carrinho particular
        if request.user.is_authenticated:
            check_exists = E_Cart.objects.filter(e_commerce=instance_obj, author=request.user).exists()
            # se ja existe o item no carrinho modifique seu valor
            if check_exists:
                update = E_Cart.objects.get(e_commerce=instance_obj)
                update.qtde += int(qtd_bought)
                update.save()
            # senão crie um carrinho particular
            else:
                E_Cart.objects.create(e_commerce=instance_obj, author=request.user, qtde=qtd_bought).save()
                del id_obj
                del qtd_bought
                del instance_obj

        # senão estiver logado adicione em uma session
        else:
            instance = {'e_commerce': id_obj, 'qtde': qtd_bought}
            if request.session.get('cart_session') is None:
                request.session['cart_session'] = [instance]
                print("CRIA ", request.session['cart_session'])
            else:

                request.session['cart_session'].append(instance)
                print("ADD ", request.session['cart_session'])


    def get_full_cart(self, request):
        if request.user.is_authenticated:
            return E_Cart.objects.filter(author=request.user)
        else:
            # del request.session['cart_session']
            # como o formato que chega do session é bruto, precisa tratar
            data_to_convert = request.session.get('cart_session')
            # if request.session.get('cart_session') is not None:
            #     json_data = request.session.get('cart_session')
            #     for item in json_data: # TODO obj.e_commerce qtde
            #         data_to_convert.append({
            #             'e_commerce': E_Commerce.objects.get(pk=item['fields']['e_commerce']),
            #             'qtde': item['fields']['qtde']
            #         })

            return data_to_convert

    def remove_item_cart(self, user, id_obj):
        item = E_Cart.objects.get(user=user, e_commerce=id_obj)
        item.drop()
        return True


class E_Cart(models.Model):
    objects = Manage_cart()
    e_commerce = models.ForeignKey(E_Commerce, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    qtde = models.IntegerField()

    # def __str__(self):
    #     return self.id
    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Requests")
