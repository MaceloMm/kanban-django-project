from django.views.generic import FormView, TemplateView, View
from django.shortcuts import render
from .forms import TaskForm
from django.urls import reverse_lazy


# Create your views here.

class IndexView(FormView):

    template_name = 'index.html'
    form_class = TaskForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        print(self.request.POST)
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {
            "form": form,
            "messagem_erro": 'Por favor corriga os erros.'
        })

