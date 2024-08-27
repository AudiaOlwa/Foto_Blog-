from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from . import forms
from . import models
from django.shortcuts import get_object_or_404
from django.forms import formset_factory
from django.urls import reverse



# Create your views here.
@login_required
def home(request):
    photos = models.Photo.objects.all()
    blogs = models.Blog.objects.all()
    return render(request, 'home.html', context={'photos': photos, 'blogs': blogs})

def billet(request):
    blogs = models.Blog.objects.all()
    return render(request, 'blog/all_billet.html', context={'blogs': blogs})

#------------------------------------------------------

@login_required
@permission_required('blog.add_photo', raise_exception=True)
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form': form})
#------------------------------------------------------------------
@login_required
@permission_required('blog.add_blog', raise_exception=True)
def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    #photo_form = forms.PhotoForm()
    if request.method == 'POST':
        blog_form = forms.BlogForm(request.POST, request.FILES)
        #photo_form = forms.PhotoForm(request.POST, request.FILES)
        if blog_form.is_valid():
            
            blog = blog_form.save(commit=False)
            blog.author = request.user
            #blog.picture = picture
            blog.save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
            return redirect('home')
    context = {
        'blog_form': blog_form,
        
}
    return render(request, 'blog/create_blog_post.html', context=context)
#-------------------------------------------------------------------
@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})
#----------------------------------------------------------------------
@login_required
@permission_required('blog.change_blog', raise_exception=True)
def edit_blog(request, blog_id):

    blog = get_object_or_404(models.Blog, id=blog_id)

    edit_form = forms.BlogForm(instance=blog)

    delete_form = forms.DeleteBlogForm()

    if request.method == 'POST':

        if 'edit_blog' in request.POST:

            edit_form = forms.BlogForm(request.POST, request.FILES, instance=blog)

            if edit_form.is_valid():

                edit_form.save()

                return redirect('home')
        if 'delete_blog' in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')

    context = {

        'edit_form': edit_form,

        'delete_form': delete_form,

}

    return render(request, 'blog/edit_blog.html', context=context)
#-----------------------------------------------------------------------

@login_required
@permission_required('blog.change_photo', raise_exception=True)

def edit_photo(request, photo_id):

    photo = get_object_or_404(models.Photo, id=photo_id)

    edit_form = forms.PhotoForm(instance=photo)

    delete_form = forms.DeletePhotoForm()

    if request.method == 'POST':

        if 'edit_photo' in request.POST:

            edit_form = forms.PhotoForm(request.POST, request.FILES, instance=photo)

            if edit_form.is_valid():

                edit_form.save()

                return redirect('home')
        if 'delete_photo' in request.POST:
            delete_form = forms.DeletePhotoForm(request.POST)
            if delete_form.is_valid():
                photo.delete()
                return redirect('home')

    context = {

        'edit_form': edit_form,

        'delete_form': delete_form,

}

    return render(request, 'blog/edit_photo.html', context=context)

#---------------------------------------------------------

@login_required
@permission_required('blog.add_photo', raise_exception=True)
def create_multiple_photos(request):

    PhotoFormSet = formset_factory(forms.PhotoForm, extra=3)

    formset = PhotoFormSet()

    if request.method == 'POST':

        formset = PhotoFormSet(request.POST, request.FILES)

        if formset.is_valid():

            for form in formset:

                if form.cleaned_data:

                    photo = form.save(commit=False)

                    photo.uploader = request.user

                    photo.save()

            return redirect('home')

    return render(request, 'blog/create_multiple_photos.html', {'formset': formset})
#--------------------------------------------------------

@login_required
def create_multiple_blogs(request):
    MultipleBlogFormSet = formset_factory(forms.MultipleBlogForm, extra=3)

    if request.method == 'POST':
        formset = MultipleBlogFormSet(request.POST, request.FILES)
        
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    # Récupérer l'image du formulaire soumis
                    picture = form.cleaned_data.get('picture')
                    blog = form.save(commit=False)
                    blog.author = request.user
                    # Assurez-vous que picture est défini avant de l'attribuer à blog.picture
                    if picture:
                        blog.picture = picture
                    blog.save()
            return redirect('home')
    else:
        formset = MultipleBlogFormSet()

    return render(request, 'blog/create_multiple_blogs.html', {'formset': formset})

@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'blog/follow_users_form.html', context={'form': form})