from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .forms import ImportLedenForm

class ImportLedenView(View):
    form_class = ImportLedenForm
    success_url = reverse_lazy('jarrbo_contributie:import')
    template_name = 'jarrbo_contributie/import_leden.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})