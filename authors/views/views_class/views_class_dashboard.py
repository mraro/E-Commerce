import os
import dotenv

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

from authors.forms import EditObjectForm
from store import models
from store.models import E_Commerce

dotenv.load_dotenv()
# THIS DECORATOR IS UTIL LIKE A FUNC BASE TO VIEW, BUT HERE WE HAVE TO USER @method_decorator and in the end use
# name='dispatch' to refer where @login_required will be affecting (dispatch is in doc of django)
@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class BaseObjectClassedView(View):
    def get_objects_to_view(self, id_obj):
        """ THIS WILL RENDER A FORM OF 'OBJECTS' TO EDIT """
        return models.E_Commerce.objects.filter(id=id_obj, author=self.request.user).first()
        # return models.E_Commerce.objects.filter(id=id_obj, is_available=False, author=self.request.user).first() # old method

    def render_view(self, form, id):  # noqa
        """ RENDER TO VIEW, NEED A FORM """
        if id is not None:
            title_site = _('Edit')
        else:
            title_site = _('Create')
        nameSite = str(os.environ.get("NAME_ENTERPRISE", "No name"))
        return render(self.request, 'pages/edit_obj_view.html', context={
            'form': form,
            'form_button': _('Save'),
            'edit': 'tru',
            'title': title_site,
            'nameSite': nameSite,
        })

    def get(self, request, pk=None):
        """ WHEN HAS A GET DATA TO USE """
        goods = self.get_objects_to_view(pk)
        print(goods)
        form = EditObjectForm(  # EditObjectForm is class made to load fields, clean e some think else
            instance=goods  # fill the fields with sent data
        )
        return self.render_view(form, pk)

    def post(self, request, pk=None):
        goods = self.get_objects_to_view(pk)
        author = models.User.objects.get(username=request.user)

        form = EditObjectForm(
            data=request.POST or None,  # receive a request data or none
            files=request.FILES or None,
            instance=goods  # if none receive what will be edited
        )
        print(pk)
        if form.is_valid():
            object_data = form.save(commit=False)
            # object_data.is_available = False
            object_data.author = author
            object_data.save()

            if pk is not None:
                messages.success(request, _('Product Saved'))
            else:
                messages.success(request, _('Product created and send to analise'))

            return redirect(reverse('authors:dashboard'))

        return self.render_view(form, pk)


@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class ObjectClassedViewDelete(BaseObjectClassedView):
    def get(self, *args, **kwargs):
        raise Http404

    def post(self, *args, **kwargs):

        goods = self.get_objects_to_view(kwargs['pk'])
        titulo = goods.title

        translated_success = _('deleted')
        translated_fail = _("wasn't deleted")
        if goods.delete():
            messages.success(self.request, f"{titulo} {translated_success}!")
        else:
            messages.error(self.request, f"{titulo} {translated_fail}!")

        return redirect(reverse('authors:dashboard'))


@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class DashboardView(ListView):
    model = E_Commerce  # DATABASE
    # paginate_by = None
    # paginate_orphans = 0
    context_object_name = 'goods'  # TABLE
    # page_kwarg = "page"
    ordering = ['-id']  # ORDERBY
    template_name = 'pages/dashboard.html'
    nameSite = str(os.environ.get("NAME_ENTERPRISE", "No name"))

    extra_context = {'nameSite': nameSite,}

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(author=self.request.user)
        queryLight = query.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ
        return queryLight
