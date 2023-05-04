from django.shortcuts import render, redirect
from django.db.models import Q
from . models import Post, Category, Comment, User
from . forms import PostForm, UserForm, MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
        
    context = {'page': page}
    return render(request, "base/login-register.html", context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login-register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(Q(category__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))

    post_count = posts.count()

    categories = Category.objects.all()[0:5]

    post_comments = Comment.objects.all().filter(Q(post__category__name__icontains=q))

    context = {"posts" : posts, 'categories': categories, "post_count" : post_count, "post_comments" : post_comments}
    return render(request, "base/home.html", context)

def post(request, pk):
    
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all()
    participants = post.participants.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = Comment.objects.create(user=request.user, post=post, body=request.POST.get('body'))
            post.participants.add(request.user)
            return redirect('post', pk=post.id)
        else:
            return redirect('login')

    context = {'post': post, 'post_comments' : post_comments, 'participants': participants}
    return render(request, "base/post.html", context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    post_comments = user.comment_set.all()
    categories = Category.objects.all()

    context = {'user': user, 'posts': posts, 'post_comments': post_comments, 'categories': categories}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)

        Post.objects.create(host=request.user, category=category, name=request.POST.get('name'), description=request.POST.get('description'))
        return redirect('home')
        
    context = {'form': form, 'categories' : categories}
    return render(request, 'base/post-form.html', context)

@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    categories = Category.objects.all()

    if request.user != post.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        post.name = request.POST.get('name')
        post.category = category
        post.description = request.POST.get('description')
        post.save()
        return redirect('home')

    context = {'form' : form, 'categories' : categories, 'post' : post}
    return render(request, "base/post-form.html", context)

@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':post})

@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':comment})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form' : form})


def categoriesPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.filter(name__icontains=q)
    return render(request, 'base/categories.html', {'categories': categories})


def activityPage(request):
    post_comments = Comment.objects.all()
    return render(request, 'base/activity.html', {'post_comments': post_comments})