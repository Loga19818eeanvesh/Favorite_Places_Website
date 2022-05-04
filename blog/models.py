
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.caption}"

class Post(models.Model):
    title = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images")
    date = models.DateField(auto_now=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    slug = models.SlugField(unique=True,db_index=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    author = models.ForeignKey(User,related_name="posts",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}({self.slug})"

class Comment(models.Model):
    user = models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")



