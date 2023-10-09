from django.contrib import messages

from store.models import E_Cart, E_Commerce
import os
import dotenv
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

dotenv.load_dotenv()


class Base_Global_Objects:
    store_name = str(os.environ.get("NAME_ENTERPRISE", "No name"))
    extra_context = {'nameSite': store_name, }

    def __init__(self):
        self.store_name = str(os.environ.get("NAME_ENTERPRISE", "No name"))

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
            else:
                cart_session = request.session['cart_session']
                # Verifique se o item já está no carrinho e atualize a quantidade
                updated = False
                for item in cart_session:
                    if item['e_commerce'] == id_obj:
                        item['qtde'] = int(item['qtde']) + int(qtd_bought)
                        updated = True
                        break
                if not updated:
                    cart_session.append(instance)
                request.session['cart_session'] = cart_session

    def get_full_cart(self, request):
        """

        :param request: data user
        :return: se logado retorna uma queryset do carrinho caso não esteja logado retorna
        um json no mesmo formato da queryset
        """

        if request.user.is_authenticated:  # se estiver authenticado ler do banco
            if request.session.get('cart_session') is not None: # se ele logou com um carrinho na session será copiado para uma qs # noqa
                json_data = request.session.get('cart_session')
                for item in json_data:  # TODO obj.e_commerce qtde
                    self.set_item_cart(request,id_obj=item['e_commerce'] ,qtd_bought=item['qtde'])
                del request.session['cart_session']
            return E_Cart.objects.filter(author=request.user)
        else:  # senão pega da session
            # del request.session['cart_session']

            data_to_converted = []
            if request.session.get('cart_session') is not None:
                json_data = request.session.get('cart_session')
                for item in json_data:  # TODO obj.e_commerce qtde
                    # breakpoint()
                    data_to_converted.append({
                        'e_commerce': E_Commerce.objects.get(pk=item['e_commerce']),
                        'qtde': item['qtde']
                    })
            return data_to_converted

    def update_item_cart(self, request):
        """ descrião:
        com as variaveis declaradas no escopo da função
        verifica se esta logado ou não o usuario, se não estiver ele vai deletar da session,
        ou se o valor novo não for igual a 0 ele vai atualizar

        se estiver logado tudo será feito por quertset na mesma logica de alguem não logado
         """

        updated = False
        deleted = False
        translated_success_upd = _('updated')
        translated_success_del = _('deleted')
        translated_fail = _("wasn't updated")
        id_to_update = request.POST.get('id-obj-to-update')
        qtde_int = int(request.POST.get('qtd'))
        if qtde_int < 0:
            qtde_int = 0
        title_obj = E_Commerce.objects.get(pk=id_to_update).title

        if request.user.is_authenticated:  # se estiver authenticado ler do banco
            goods = E_Cart.objects.get(e_commerce_id=id_to_update, author=request.user)
            if qtde_int == 0:
                goods.delete()
                deleted = True

            else:
                try:
                    goods.qtde = qtde_int
                    goods.save()
                    updated = True
                except:
                    pass
        else:  # not authenticated

            cart_session = request.session['cart_session']
            # Verifique se o item já está no carrinho e atualize a quantidade
            new_cart = []

            for item in cart_session:
                if item['e_commerce'] != id_to_update:
                    new_cart.append(item)

                else:
                    if qtde_int == 0:
                        deleted = True
                    else:
                        item['qtde'] = qtde_int

                        updated = True
                        new_cart.append(item)

            request.session['cart_session'] = new_cart

        if updated or deleted:
            if updated:
                messages.success(request, f"{title_obj} {translated_success_upd}!")
            else:
                messages.error(request, f"{title_obj} {translated_success_del}!")

        else:
            messages.error(request, f"{title_obj} {translated_fail}!")
