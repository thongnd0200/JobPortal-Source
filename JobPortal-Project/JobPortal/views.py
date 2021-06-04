from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from .forms import *

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        candidates = Candidates.objects.filter(
            company__name=request.user.company.name)
        context = {
            'candidates': candidates,
        }
        return render(request, 'hr.html', context)
    else:
        companies = Company.objects.all()
        context = {
            'companies': companies,
        }
        return render(request, 'Jobseeker.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'login.html')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                currUser = form.save()
                Company.objects.create(user=currUser, name=currUser.username)
                return redirect('login')
        context = {
            'form': form
        }
        return render(request, 'register.html', context)


def updateJob(request):
    if request.user.is_authenticated:
        company = request.user.company
        form = CompanyForm(instance=company)
        if request.method == 'POST':
            form = CompanyForm(request.POST, instance=company)
            if form.is_valid:
                form.save()
                return redirect('/')
        context = {
            'form': form
        }
        return render(request, 'updateJob.html', context)
    else:
        return redirect('login')


def applyPage(request, id):
    company = Company.objects.get(id=id)
    candidate, created = Candidates.objects.get_or_create(name='Your name', company=company)
    form = ApplyForm(instance=candidate)
    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'apply.html', context)
