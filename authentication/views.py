from django.shortcuts import redirect, render
#from django.contrib.auth import logout
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import UploadProfilePhotoForm
from . import forms 
from . import models
# Create your views here.


def logout_user(request):
    logout(request)
    return redirect('login')

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method =='POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],

            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'login.html', context={'form': form, 'message': message})

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'authentication/signup.html', context={'form': form} )  

@login_required
def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm()
    if request.method == 'POST':
        form = UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UploadProfilePhotoForm(instance=request.user)
    return render(request, 'upload_profile_photo.html', context={'form': form})

#def upload_profile_photo(request):
#    form = forms.UploadProfilePhotoForm()
#    if request.method == 'POST':
#        form = forms.UploadProfilePhotoForm(request.POST, request.FILES)
#        if form.is_valid():
#            profile_photo = form.save(commit=False)
#            # set the uploader to the user before saving the model
#            profile_photo.uploader = request.user
#            # now we can save
#            profile_photo.save()
#            return redirect('home')
#    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})
