from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.template import loader
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.urls import reverse
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

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    total_likes = blog.totalLikes()
    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        liked = True
    if request.method =="POST":
        form = CommentForm(data=request.POST)
        new_comment = form.save(commit=False)
        new_comment.blog = blog
        new_comment.save()
        return HttpResponseRedirect(reverse('blogpost', args=[str(blog.slug)]))
    else:
        form = CommentForm()
    context = {'blog': blog, "total_likes" : total_likes, "liked" : liked, 'form':form}
    return render(request, 'blogcontent.html',context)

def blogpage(request):
    if request.method == "POST":
        sort_type = request.POST.get('sort')
        order = request.POST.get('order')
        blogs = Blog.objects.all().order_by(order+sort_type)
    else:
        blogs = Blog.objects.all()
    paginator = Paginator(blogs, 20)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    if page == None:
        page = 1
    elided_pages = paginator.get_elided_page_range(number=page, on_each_side=2, on_ends=0)
    context = {'blogs': blogs, 'elided_pages' : elided_pages}
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
    fields = ['title', 'image', 'description','content']
    
    def form_valid(self, form):
        form.instance.user_name = self.request.user
        template_name = 'blog_form.html'
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().form_valid(form)

@login_required
def update_blog(request, id):
    blog = Blog.objects.get(serial_num=id)
    if request.method=="POST":
        form = BlogForm(instance=blog, data=request.POST, files=request.FILES)
        if form.is_valid():
            
            
            form.save()
            messages.success(request,"Blog has been succesfully updated!")
            return redirect('blogpost',blog.slug)
    else:
        form = BlogForm(instance=blog)
    context = {
        'form':form,
        'blog':blog
    }
    return render(request, 'blog_form.html', context)

@login_required
def delete_blog(request, id):
    blog = Blog.objects.get(serial_num=id)
    blog.delete()
    messages.success(request,"Blog has been succesfully deleted!")
    return redirect('userblogs')

@login_required
def edit(request):
    if request.method=='POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile) 
    return render(request, 'edit.html', {"user_form":user_form, "profile_form":profile_form})

@login_required
def user_blogs(request):
    current_user = request.user
    blogs = Blog.objects.filter(user_name=current_user)
    return render(request, 'user/user_blogs.html', {'blogs':blogs})
@login_required
def LikeView(request, id):
    blog = get_object_or_404(Blog, serial_num=request.POST.get('serial_num'))
    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        liked = False
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('blogpost', args=[str(blog.slug)]))
