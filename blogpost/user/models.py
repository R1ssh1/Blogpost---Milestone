from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
from tinymce.models import HTMLField
from blogpost import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg',upload_to='profile_pictures')
    description = models.CharField(default="A long time ago, In a galaxy far far away...",max_length=100)
    def __str__(self):
        return self.user.username
class Blog(models.Model):
    serial_num = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = HTMLField()
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    likes = models.ManyToManyField(User, related_name='blogs_liked', blank=True)
    image= models.ImageField(default='blogpic.jpg', upload_to='blog_thumbnails')
    description = models.CharField(max_length=40, default="default blog description...")
    def totalLikes(self):
        return self.likes.count()
    def __str__(self):
        return self.title
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Blog.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.slug)])
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE, default=1)
    body = RichTextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return '%s - %s' % (self.blog.title, self.user.username)