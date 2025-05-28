from django.urls import path
from .views import IndexView, UpdateTask, LoginView, SingUpView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('update_task/<int:task_id>/', UpdateTask.as_view(), name='update_task_status'),
    path('login/', LoginView.as_view(), name='login'),
    path('singup/', SingUpView.as_view(), name='singup'),
    path('logout/', LogoutView.as_view(), name='logout')
]