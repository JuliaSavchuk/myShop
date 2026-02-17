from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from main.models import Category

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url if next_url else 'main:product_list')
    else:
        form = AuthenticationForm()
    categories = Category.objects.all()
    return render(request, 'accounts/login.html', {'form': form, 'categories': categories})

def logout_view(request):
    logout(request)
    return redirect('main:product_list')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:product_list')
    else:
        form = UserCreationForm()
    categories = Category.objects.all()
    return render(request, 'accounts/register.html', {'form': form, 'categories': categories})

@login_required
def profile_view(request):
    categories = Category.objects.all()
    return render(request, 'accounts/profile.html', {'categories': categories})

class AdminAccessRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect('main:product_list')
        return self.get_response(request)