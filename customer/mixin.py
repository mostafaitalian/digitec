from django.shortcuts import get_object_or_404
from .models import Customer
from django.utils.functional import cached_property
from django.contrib import messages
class CustemerGetObjectMixin:
    
    def get_object(self, id):
        obj = get_object_or_404(Customer, id=id)
        return obj
class CustemerGetObject1Mixin:
    
    def get_object(self):
        id = self.kwargs.get('id')
        obj = get_object_or_404(Customer, pk=id)
        return obj
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        total = 0 
        if self.object.departments:
            for dep in self.object.departments.all():
                if dep.no_of_machine:
                    total +=dep.no_of_machine
        context['total_machine'] = total
        return context
class CustomerLikesUpdateMixin:
    @cached_property
    def likes_favorite(self):
        likes = self.object.like()
        favorites = self.object.favorite()
        favorite_count = favorites.count()
        return {'likes':likes,'favorites':favorites,'favorite_count':favorite_count}
class CustomerActionMixin:
    @property
    def success_msg(self):
        return 'customer is updated-'
    def form_valid(self,form):
        slug = form.cleaned_data['slug']
        customer = form.save()
        print(slug)
        id = self.kwargs.get('id', -1)
        # self.slug=slug
        #self.request.kwargs['slug']=slug
        if id == -1:
            self.id = customer.id
        else:
            self.id = id    
        self.kwargs.update({'slug_kwargs':slug})
        messages.info(self.request, self.success_msg)
        return super().form_valid(form)