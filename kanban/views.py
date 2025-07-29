import datetime
import django.contrib.auth.models
from django.utils import timezone
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import TaskForm
from .models import Task, Profile
from datetime import datetime
import json
from django.urls import reverse_lazy


# Create your views here.

class IndexView(LoginRequiredMixin, View):
    template_name = 'index.html'
    form = TaskForm()

    @staticmethod
    def get_tasks(context: dict, request) -> dict:
        tasks = Task.objects.filter(status=True, profile__user=request.user.id).order_by('create')
        if 'tasks_today' in request.GET and request.GET['tasks_today']:
            tasks = [i for i in tasks if i.create.date() == timezone.now().date()]
        elif 'data_customer' in request.GET and request.GET['data_customer']:
            date = request.GET.get('data_customer')
            date = [int(n) for n in date.split('-')]
            tasks = [i for i in tasks if i.create.date() == datetime(year=date[0], month=date[1], day=date[2]).date()]
        context.update({'tasks_ni': [i for i in tasks if i.task_status == 'NI'],
                        'tasks_ea': [i for i in tasks if i.task_status == 'EA'],
                        'tasks_cl': [i for i in tasks if i.task_status == 'CL'],
                        'quantity_tasks': len(Task.objects.filter(status=True)),
                        'user': Profile.objects.get(user=request.user.id)
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
            form.save(request=request)
            return redirect('index')
        return render(request, template_name=self.template_name, context=self.get_tasks({'form': self.form}, request))


class UpdateTask(View):

    def post(self, request, task_id):
        try:
            edit_task = Task.objects.get(id=task_id)
            edit_task.task_status = json.loads(request.body).get('status')
            edit_task.save()
            return JsonResponse({'sucess': True})
        except Task.DoesNotExist:
            return JsonResponse({'sucess': False, 'message': 'Tarefa não existe'})
        except Exception as e:
            print(f'Erro: {e}')
            return JsonResponse({'sucess': False, 'message': 'Ocorreu um erro'})


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, template_name=self.template_name)

    def post(self, request):
        try:
            user = User.objects.get(email=request.POST.get('email'))
            print(user.email)
        except django.contrib.auth.models.User.DoesNotExist:
            return render(request, template_name=self.template_name, context={'message': 'Usuario ou Senha invalido!'})
        else:
            if authenticate(username=user.username, password=request.POST.get('password')):
                login(request, authenticate(username=user.username, password=request.POST.get('password')))
                return redirect('index')
            return render(request, template_name=self.template_name, context={'message': 'Usuario ou Senha invalido!'})


class SingUpView(View):
    template = 'singin.html'

    def get(self, request):
        return render(request, template_name=self.template)


class UserView(View, LoginRequiredMixin):
    template = 'profile.html'

    def get(self, request):
        prof = Profile.objects.get(user=request.user.id)
        total = Task.objects.filter(profile=prof.id)
        return render(request, template_name=self.template, context={'user': prof,
                                                                     'total': len(total),
                                                                     'cl': len(total.filter(task_status='CL'))
                                                                     })