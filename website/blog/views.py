from django.utils import timezone
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View
from django.db.models import Q  # Імпортуйте Q для використання в фільтрах

from .forms import PostForm, PostImageFormSet, UserRegistrationForm, ProfileUpdateForm, CommentForm, SubscribeForm, PhotoForm, ProfileForm
from .models import Post, Category, Profile, Comment, Photo, Subscriber, PostImage

def get_categories():
    all_categories = Category.objects.all()
    count = all_categories.count()
    half = count // 2
    first_half = all_categories[:half]
    second_half = all_categories[half:]
    return {'cats1': first_half, 'cats2': second_half}

def index(request):
    posts = Post.objects.all().order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)

def category(request, c=None):
    cObj = get_object_or_404(Category, name=c)
    posts = Post.objects.filter(category=cObj).order_by("-published_date")
    context = {'posts': posts, 'category': cObj}
    context.update(get_categories())
    return render(request, "blog/index.html", context)

def post(request, name=None):
    post = get_object_or_404(Post, title=name)
    comments = Comment.objects.filter(post=post).order_by('-published_date')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post', name=post.title)
    else:
        comment_form = CommentForm()
    
    context = {'post': post, 'comments': comments, 'comment_form': comment_form}
    context.update(get_categories())
    return render(request, "blog/post.html", context)

def contact(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not Subscriber.objects.filter(email=email).exists():
                form.save()
                return redirect('contact')
            else:
                context = {'form': form, 'error': 'This email is already subscribed.'}
                return render(request, 'blog/contact.html', context)
    else:
        form = SubscribeForm()
    
    context = {'form': form}
    return render(request, 'blog/contact.html', context)

def search(request):
    query = request.GET.get('query')
    if query:
        posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    else:
        posts = Post.objects.none()  # Повертаємо порожній QuerySet, якщо запит порожній

    context = {'posts': posts, 'query': query}
    context.update(get_categories())
    return render(request, "blog/index.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        image_formset = PostImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())

        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            post_form.save_m2m()  # Save tags after saving the post

            for form in image_formset:
                if form.cleaned_data.get('DELETE'):
                    continue
                if form.cleaned_data:
                    image = form.cleaned_data['image']
                    PostImage.objects.create(post=post, image=image)

            return redirect('blog:index')
    else:
        post_form = PostForm()
        image_formset = PostImageFormSet(queryset=PostImage.objects.none())

    context = {
        'post_form': post_form,
        'image_formset': image_formset,
    }

    context.update(get_categories())
    return render(request, "blog/create.html", context)

class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('blog:index')

@login_required
def edit_profile(request):
    profile_instance, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile_instance)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile_instance)
    context = {"form": form}
    context.update(get_categories())
    return render(request, 'blog/profileUpdate.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('blog:profile')
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, 'blog/registration.html', context)

def user_profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'blog/user_profiles.html', context)

def gallery(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo_form.save()
            return redirect("media")
    else:
        photo_form = PhotoForm()
    return render(request, "gallery/media.html", {"form": photo_form, "photos": photos})

@login_required
def profile(request):
    profile_data = Profile.objects.get(user=request.user)
    current_time = timezone.now()
    user_stats = {
        'comments_count': request.user.comment_set.count(),
        'posts_count': request.user.post_set.count(),
        'days_on_site': (current_time - request.user.date_joined).days,
        'reputation': profile_data.reputation,
    }
    context = {
        'user': request.user,
        'profile_data': profile_data,
        'user_stats': user_stats,
    }
    return render(request, 'blog/profile.html', context)

@login_required
def edit_profile(request):
    profile_instance, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile_instance)
    
    context = {"form": form}
    return render(request, 'blog/profileupdate.html', context)

def comment_upvote(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.upvote()
    return redirect('blog:post', name=comment.post.title)

def comment_downvote(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.downvote()
    return redirect('blog:post', name=comment.post.title)