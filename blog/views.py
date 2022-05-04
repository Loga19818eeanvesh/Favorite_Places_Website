
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.text import slugify

from .models import Post,Tag,Comment
from .forms import CommentForm, RegisterForm, LoginForm, PostForm

# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

    '''def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context'''

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "posts"

    '''def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context'''

class PostDetailView(View):

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
          is_saved_for_later = post_id in stored_posts
        else:
          is_saved_for_later = False

        return is_saved_for_later

    def get(self,request,slug):
        try:
            post = Post.objects.get(slug=slug)
        except:
            response_data = render_to_string('404.html')
            return HttpResponseNotFound(response_data)

        return render(request,'blog/post-detail.html',{
            "post" : post,
            "post_author" : post.author,
            "tags" : post.tags.all(),
            "comments" : post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
            "comment_form" : CommentForm()
        })

    def post(self,request,slug):
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)

            try:
                post = Post.objects.get(slug=slug)
            except:
                response_data = render_to_string('404.html')
                return HttpResponseNotFound(response_data)

            if comment_form.is_valid():
                comment = Comment.objects.create(user=request.user,text=comment_form.cleaned_data['text'],post=post)
                comment.save()
                return redirect('post_detail_page',slug=slug)
            else:
                return render(request,'blog/post-detail.html',{
                    "post" : post,
                    "post_author" : post.author,
                    "tags" : post.tags.all(),
                    "comments" : post.comments.all().order_by("-id"),
                    "saved_for_later": self.is_stored_post(request, post.id),
                    "comment_form" : comment_form
                })
        else:
            response_data = render_to_string('404.html')
            return HttpResponseNotFound(response_data)

def user_posts(request,id):
    try:
        user = User.objects.get(id=id)
    except:
        response_data = render_to_string('404.html')
        return HttpResponseNotFound(response_data)

    posts = user.posts.all()

    return render(request,'blog/all-posts.html',{
        "posts":posts,
        "user_name" : user.first_name
    })

def all_users(request):
    users = User.objects.all()

    return render(request,'blog/all-users.html',{
        "users":users
    })

    

class CreatePostView(View):
    def get(self,request):
        form = PostForm()
        return render(request,"blog/create.html",{'form':form})

    def post(self,request):
        if request.user.is_authenticated:
            post_form = PostForm(request.POST,request.FILES)
            if post_form.is_valid():
                slug = slugify(post_form.cleaned_data['slug'])
                if Post.objects.filter(slug=slug).exists():
                    return render (request, "blog/create.html", {
                    'form':post_form,
                    'message':"slug already taken."
                    })
                post = Post.objects.create(title=post_form.cleaned_data['title'],address=post_form.cleaned_data['address'],image=post_form.cleaned_data['image'],content=post_form.cleaned_data['content'],slug=slug,author=request.user) 
                post.save()
                return redirect('starting_page')
            else:
                return render(request,'blog/create.html',{
                    "form" : post_form
                })
        else:
            response_data = render_to_string('404.html')
            return HttpResponseNotFound(response_data)


class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render (request, "blog/login.html", {'form':form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            user = authenticate(username=user_name,password=password)
            if user is not None:
                login(request, user)
                return redirect('starting_page')
            else:
               return render (request, "blog/login.html", {
                   'form':form,
                   'message':"Invalid Credentials"
                })
        return render (request, "blog/login.html", {'form':form})


class RegisterView(View):
    def get(self,request):
        form = RegisterForm()
        return render (request, "blog/register.html", {'form':form})

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_email = form.cleaned_data['user_email']
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']
            if(password!=password1):
                return render (request, "blog/register.html", {
                'form':form,
                'message':"Passwords Not matching"
                })
            if User.objects.filter(username=user_name).exists():
                return render (request, "blog/register.html", {
                'form':form,
                'message':"Username already taken."
                })
            if User.objects.filter(email=user_email).exists():
                return render (request, "blog/register.html", {
                'form':form,
                'message':"Email already taken."
                })

            user = User.objects.create_user(username=user_name,password=password,email=user_email,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('login')
        
        return render (request, "blog/register.html", {'form':form})


def logout_view(request):
    logout(request)
    return redirect('starting_page')

class DeletePostView(View):
    def get(self,request):
        response_data = render_to_string('404.html')
        return HttpResponseNotFound(response_data)

    def post(self,request):
        post_id = request.POST["post_id"]
        try:
            post = Post.objects.get(id=post_id)
        except:
            response_data = render_to_string('404.html')
            return HttpResponseNotFound(response_data)
        post.delete()
        return redirect('starting_page')
               

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
          posts = Post.objects.filter(id__in=stored_posts)
          context["posts"] = posts
          context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
          stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
          stored_posts.append(post_id)
        else:
          stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")


class PostDetailView1(DetailView):
    template_name = "blog/post-detail.html"
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["tags"] = self.object.tags.all()
        context["comment_form"] = CommentForm()
        return context


def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request,'blog/index.html',{
        "posts" : latest_posts
    })

def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request,'blog/all-posts.html',{
        "posts" : all_posts
    })

def post_datail(request,slug):

    try:
        post = Post.objects.get(slug=slug)
    except:
        response_data = render_to_string('404.html')
        return HttpResponseNotFound(response_data)

    return render(request,'blog/post-detail.html',{
        "post" : post,
        "tags" : post.tags.all()
    })

