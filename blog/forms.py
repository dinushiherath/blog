from django import forms
from .models import Post, Comment, Image, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'images', 'text', 'tags')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('name', 'image')


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', )



