import datetime
from django.utils import timezone
from django.views.generic import FormView, TemplateView, View
from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task
from django.urls import reverse_lazy


# Create your views here.

class IndexView(View):
    template_name = 'index.html'
    form = TaskForm()

    @staticmethod
    def get_tasks(context: dict, request) -> dict:
        tasks = Task.objects.filter(status=True).order_by('create')
        if 'tasks_today' in request.GET:
            tasks = [i for i in tasks if i.create.strftime('%d%m%Y') == timezone.now().strftime('%d%m%Y')]
        context.update({'tasks_ni': [i for i in tasks if i.task_status == 'NI'],
                        'tasks_ea': [i for i in tasks if i.task_status == 'EA'],
                        'tasks_cl': [i for i in tasks if i.task_status == 'CL'],
                        'quantity_tasks': len(tasks)
                        })
        return context

    def get_task(self) -> Task:
        return Task.objects.get(id=int(self.request.POST.get('tarefa_id')[0]))

    def get(self, request):
        return render(request, template_name=self.template_name, context=self.get_tasks({'form': self.form}, request))

    def post(self, request):

        if 'deleteMethod' in request.POST:
            deleted_item = self.get_task()
            deleted_item.status = False
            deleted_item.save()
            return render(request, template_name=self.template_name,
                          context=self.get_tasks({'form': self.form, 'message': 'Tarefa excluida com Sucesso!'}, request))

        elif 'editTask' in request.POST:
            item_edit = self.get_task()
            item_edit.title = request.POST.get('title')
            item_edit.description = request.POST.get('description')
            item_edit.save()
            return redirect('index')

        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, template_name=self.template_name, context=self.get_tasks({'form': self.form}, request))

