from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class ApplyForm(ModelForm):
    class Meta:
        model = Candidates
        fields = "__all__" 


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['user']