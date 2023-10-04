from store.models import E_Cart, E_Commerce
import os
import dotenv

dotenv.load_dotenv()

class Base_Global_Objects:

    store_name = str(os.environ.get("NAME_ENTERPRISE", "No name"))
    extra_context = {'nameSite': store_name, }

    def __init__(self):
        self.store_name = str(os.environ.get("NAME_ENTERPRISE", "No name"))

    def set_item_cart(self, request, id_obj, qtd_bought):
        print("SET ITEM")
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
        print("GET ITEM")

        if request.user.is_authenticated:  # se estiver authenticado ler do banco
            return E_Cart.objects.filter(author=request.user)
        else:  # senão pega da session
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
            # print("IN GET ", request.session['cart_session'])
            return data_to_convert

    def remove_item_cart(self, user, id_obj):
        item = E_Cart.objects.get(user=user, e_commerce=id_obj)
        item.drop()
        return True