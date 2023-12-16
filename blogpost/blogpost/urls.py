"""
URL configuration for blogpost project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user.urls')),
    path('', user_views.homepage, name='home'),
    path('signup/', user_views.signup, name='signup' ),
    path('blogpage/<str:slug>/', user_views.blogpost, name='blogpost'),
    path('blogpage/', user_views.blogpage, name='blogpage'),
    path('login/',auth_views.LoginView.as_view(template_name='loginpage.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logoutpage.html'),name='logout'),
    path('profile/',user_views.profile, name='profile'),
    path('addblog/',user_views.CreateBlog.as_view(), name='createblog'),
    path('update/<int:id>/', user_views.update_blog, name='updateblog'),
    path('delete/<int:id>', user_views.delete_blog, name='deleteblog'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name="change_password_form.html"), name='change_password'),
    path('change_password_done/', auth_views.PasswordChangeDoneView.as_view(template_name="change_password_done.html"), name="change_password_done"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name = "password_reset_complete"),
    path('profile/edit/', user_views.edit, name='edit'),
    path('tinymce/', include('tinymce.urls')),
    path('about/', user_views.about, name='about'),
    path('contact/', user_views.contact, name='contact')
]   

urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
