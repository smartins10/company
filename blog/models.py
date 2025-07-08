from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinLengthValidator



# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=150)
    resume = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts", null="True")
    date = models.DateField(auto_now=True)
    slug = AutoSlugField(populate_from = 'title', unique = True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='posts')
    tag = models.ManyToManyField('Tag', related_name='posts')

    def __str__(self):
        return self.title  

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    caption = models.CharField(max_length=20)    

    def __str__(self):
        return self.caption    
    
class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

 