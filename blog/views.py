from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Image, Tag
from .forms import PostForm, CommentForm, ImageForm, TagForm
from django.db.models import Q


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_search_view(request):
    search_term = request.GET.get('search_term')
    tag = request.GET.get('tag')
    if search_term:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(
            Q(title__icontains=search_term) | Q(text__icontains=search_term) | Q(
                tags__name__icontains=search_term)).order_by('published_date')
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(tags__in=[tag]).order_by(
            'published_date')
    return render(request, 'blog/blog_search_list_view.html', {'posts': posts, 'search_term': search_term or tag})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required()
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        tag = TagForm
        return render(request, 'blog/post_edit.html', {'form': form, 'tag': tag})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def add_images(request):
    if request.method == "POST":
        if 'save' in request.POST:
            image_form = ImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                image_form.save()
                return redirect('add_images')
        elif 'delete' in request.POST:
            image_list = request.POST.getlist('select_image')
            for image_number in image_list:
                image = get_object_or_404(Image, pk=image_number)
                image.delete()
            return redirect('add_images')
    else:
        image_form = ImageForm()
        images = Image.objects.all()
    return render(request, 'blog/add_images.html', {'image_form': image_form, 'images': images})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = TagForm()
        return render(request, 'blog/add_tag.html', {'form': form})
