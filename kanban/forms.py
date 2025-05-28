from django import forms
from .models import Task, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'task_status']


class CustomUserCreationForm(UserCreationForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            Profile.objects.create(user=user, image=self.cleaned_data.get('image'))
        return user
