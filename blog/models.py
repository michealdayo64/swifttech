from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published')
)

CATEGORY_CHOICES = (
    ('tech', 'Tech'),
    ('education', 'Education'),
    ('product', 'Product')
)

class Authur(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField()

    def __str__(self):
        return self.user.username

#class Category(models.Model):
#    title = models.CharField(max_length=50)

#   def __str__(self):
#       return self.title

class Post(models.Model):
    categories = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    title = models.CharField(max_length=200)
    descriptions = models.TextField()
    slug = models.SlugField()
    image = models.ImageField()
    author = models.ForeignKey(Authur, on_delete=models.CASCADE, related_name='author')
    #thumbnail = models.ImageField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[
            #self.publish.year,
            #self.publish.strftime('%m'),
            #self.publish.strftime('%d'),
            self.slug
        ])

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Comment by {} of {}'.format(self.name, self.post)

class Newletter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email