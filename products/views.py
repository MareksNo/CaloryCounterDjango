from products.models import Food
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, edit


class CreateFoodView(edit.CreateView):
    model = Food
    fields = ['name', 'description', 'calories',]

    def get(self, *args, **kwargs):
        if not self.request.user.has_perm('products.add_food'):
            return HttpResponseRedirect(reverse('login'))

        return super().get(request=self.request)

    def get_success_url(self):
        return reverse('login')
