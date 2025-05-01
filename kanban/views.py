from django.views.generic import FormView, TemplateView, View
from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task
from django.urls import reverse_lazy


# Create your views here.

class IndexView(View):
    template_name = 'index.html'
    form = TaskForm()
    tasks = Task.objects.filter(status=True)

    def get(self, request):
        return render(request,
                      template_name=self.template_name,
                      context={
                          'tasks_ni': [i for i in self.tasks if i.task_status == 'NI'],
                          'tasks_ea': [i for i in self.tasks if i.task_status == 'EA'],
                          'tasks_cl': [i for i in self.tasks if i.task_status == 'CL'],
                          'form': self.form,
                      })

    def post(self, request):

        if 'deleteMethod' in request.POST:
            item_id = int(request.POST.get('tarefa_id')[0])
            if Task.objects.filter(id=item_id).exists():
                deleted_item = Task.objects.get(id=item_id)
                deleted_item.status = False
                deleted_item.save()
                self.tasks = Task.objects.filter(status=True)
                return render(request,
                              template_name=self.template_name,
                              context={
                                    'tasks': self.tasks,
                                    'form': self.form,
                                    'message': 'Tarefa excluida com Sucesso!',
                                    'tasks_ni': [i for i in self.tasks if i.task_status == 'NI'],
                                    'tasks_ea': [i for i in self.tasks if i.task_status == 'EA'],
                                    'tasks_cl': [i for i in self.tasks if i.task_status == 'CL']
                              })
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, template_name=self.template_name, context={'tasks': self.tasks, 'form': self.form})

