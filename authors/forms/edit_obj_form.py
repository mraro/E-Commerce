# DOC https://docs.djangoproject.com/en/4.1/ref/forms/fields/
import json
import time

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

from store.models import E_Commerce, Covers

from commerce.settings import BASE_DIR


class EditObjectForm(forms.ModelForm):
    """ can you pass args to fill the fields, a dict with same name key with (instance="dict") """

        # add_attr(self.fields.get('slug'), 'type', 'hidden')

    title = forms.CharField(min_length=4, max_length=65, label=_('Title'))
    slug = forms.CharField(widget=forms.HiddenInput(), empty_value=" ", label="")  # HERE I HAD TO GIVE SOME FAKE DATA
    # TO DJANGO SEND FORM PROPERLY, IN ORDER TO MAKE A SLUGFY LATER, BEFORE SEND TO IS_VALID
    price = forms.DecimalField(min_value=0.00, max_value=100000.00, decimal_places=2, label=_('Price'))
    quantity = forms.IntegerField(min_value=1, max_value=1000000, label=_('Quantity'))
    cover = forms.FileField(widget=forms.TextInput(attrs={
        "name": "images",
        "type": "File",
        "class": "form-control",
        "multiple": "True",
    }), label="", required=False)
    # cover = forms.ClearableFileInput(attrs={'multiple': True})

    def clean_slug(self):
        # print("Clean Slug")
        data = slugify(self.cleaned_data.get('title'))
        # exists = Remedios.objects.filter(slug=data).exists()

        while E_Commerce.objects.filter(slug=data).exists():
            data += "X"
            # THIS IS A DANGEROUS FORM TO GRANT THAT NEVER HAS SAME SLUG
            # raise ValidationError('My unique field should be unique.')
        return data

    def clean_title(self):
        title = self.cleaned_data.get('title')
        exist = E_Commerce.objects.filter(title=title).exists()
        if exist:
            raise ValidationError(_('This Title already in use'))
        return title

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     files = self.cleaned_data['files']
    #     multiview_images = []
    #     print(instance," - ", files)
    #     for file in files:
    #         # Gere um nome único para cada arquivo, por exemplo, usando um timestamp
    #         filename = f"imagem_{(self.title)}_{file.name}"
    #         # Especifique o caminho onde deseja salvar os arquivos localmente
    #         filepath = BASE_DIR.join("covers/", filename)
    #
    #         # Salve o arquivo no sistema de arquivos local
    #         with open(filepath, 'wb') as destination:
    #             for chunk in file.chunks():
    #                 destination.write(chunk)
    #
    #         # Adicione o caminho do arquivo ao seu modelo ou lista de imagens
    #         multiview_images.append(filepath)
    #
    #     # Salve os caminhos das imagens em seu modelo ou como preferir
    #     instance.multiview_images = json.dumps(multiview_images)
    #
    #     if commit:
    #         instance.save()
    #     return instance

    class Meta:
        model = E_Commerce  # database
        fields = 'title', 'price', 'quantity', 'description', 'tags', 'category', 'composition', 'cover', 'slug',
        # exclude = []
        labels = {
            # 'title': 'Titulo: ',
            'description': _('Description: '),
            # 'price': 'Preço: ',
            'quantity': _('Quantity: '),
            'category': _('Category: '),
            'composition': _('Composition: '),
        }

        widgets = {

            # 'cover': forms.FileInput(
            #     attrs={
            #         'class': 'image-object',
            #         'onchange': "previewImagem()",
            #     }
            # ),
            # 'quantity': forms.Select(attrs={'class': 'quantity-object'},
            #                          choices=(
            #                              ('0', '0'),
            #                              ('30', '30'),
            #                              ('60', '60'),
            #                              ('120', '120'),
            #                          )
            #                          )
        }
