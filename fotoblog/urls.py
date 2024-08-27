from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import authentication.views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
import blog.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    #path('', LoginView.as_view(
    #         template_name='login.html',
    #         redirect_authenticated_user=True), name='login'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('home', blog.views.home, name='home'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),

         #app blog
    path('photo_upload/', blog.views.photo_upload, name='photo_upload'),
    path('change_profile_photo/', authentication.views.upload_profile_photo, name='change_profile_photo'),
    path('blog_create', blog.views.blog_and_photo_upload, name='blog_create'),
    path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'),
    path('all_blogs', blog.views.billet, name='all_blogs'),
    path('blog/<int:blog_id>/edit', blog.views.edit_blog, name='edit_blog'),
    path('photo/<int:photo_id>/edit', blog.views.edit_photo, name='edit_photo'),
    path('photo/upload-multiple/', blog.views.create_multiple_photos, name='create_multiple_photos'),
    path('upload-multiple/', blog.views.create_multiple_blogs, name='create_multiple_blogs'),
    path('follow-users/', blog.views.follow_users, name='follow_users'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

