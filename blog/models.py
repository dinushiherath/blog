import markdown
import re

from django.db import models
from django.utils import timezone


def markdown_to_html(markdown_text, images):
    for image in images:
        # image_ref = "![{}]({})".format(image.name, image.image.url)
        image_ref = '<img title="{}" src="{}" width="200">'.format(image.name, image.image.url)
        markdown_text = markdown_text.replace('![{}][]'.format(image.name), image_ref)
    html = markdown.markdown(markdown_text)
    return html


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.name

    def return_image(self):
        return markdown_to_html(self.text, self.images.all())


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    images = models.ManyToManyField(Image, blank=True)
    text = models.TextField()
    tags = models.CharField(max_length=400, default="")
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def body_html(self):
        return markdown_to_html(self.text, self.images.all())

    def body_text(self):
        text = self.text
        for image in self.images.all():
            text = text.replace('![{}][]'.format(image.name), "")
        return text

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
