from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Blog
from django.contrib.auth.models import User
from django.template import loader
from .forms import SignupForm, BlogForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
# Create your views here.

def homepage(request):
    return render(request, 'indexpage.html')

def loginpage(request):
    return render(request, 'loginpage.html')

def userlist(request):
    user_list = User.objects.all()
    context= {'user_list':user_list}
    return render(request, 'userpage.html',context)

def userdetails(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {
        'user':user,
    }
    return render(request, 'detail.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Welcome {username}, your account is created")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signuppage.html', {'form' : form})

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    context = {'blog': blog}
    return render(request, 'blogcontent.html',context)

def blogpage(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request,'blogpage.html',context)

@login_required
def profile(request):
    return render(request, 'profile.html')

def create_blog(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('blogpage')
    context = {'form':form}
    return render(request, 'blog_form.html',context)

class CreateBlog(CreateView):
    model = Blog
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.user_name = self.request.user
        template_name = 'blog_form.html'
        return super().form_valid(form)


def update_blog(request, id):
    blog = Blog.objects.get(serial_num=id)
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        form.save()
        return redirect('blogpage')
    context = {
        'form':form,
        'blog':blog
    }
    return render(request, 'blog_form.html', context)

def delete_blog(request, id):
    blog = Blog.objects.get(serial_num=id)
    if request.method == 'POST':
        blog.delete()
        return redirect('blogpage')
    context={
        'blog':blog
    }
    return render(request, 'blog_delete.html', context)