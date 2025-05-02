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
    def get_tasks(context: dict) -> dict:
        tasks = Task.objects.filter(status=True).order_by('create')
        context.update({'tasks_ni': [i for i in tasks if i.task_status == 'NI'],
                          'tasks_ea': [i for i in tasks if i.task_status == 'EA'],
                          'tasks_cl': [i for i in tasks if i.task_status == 'CL']
                        })
        return context

    def get(self, request):
        return render(request, template_name=self.template_name, context=self.get_tasks({'form': self.form}))

    def post(self, request):

        if 'deleteMethod' in request.POST:
            item_id = int(request.POST.get('tarefa_id')[0])
            if Task.objects.filter(id=item_id).exists():
                deleted_item = Task.objects.get(id=item_id)
                deleted_item.status = False
                deleted_item.save()
                return render(request, template_name=self.template_name,
                              context=self.get_tasks({'form': self.form, 'message': 'Tarefa excluida com Sucesso!'}))

        elif 'editTask' in request.POST:
            item_edit = Task.objects.get(id=int(request.POST.get('tarefa_id')))
            item_edit.title = request.POST.get('title')
            item_edit.description = request.POST.get('description')
            item_edit.save()
            return redirect('index')

        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, template_name=self.template_name, context=self.get_tasks({'form': self.form}))

