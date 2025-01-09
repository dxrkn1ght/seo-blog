from django.db import models
from django.utils.text import slugify
from django import forms
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    short_content = models.TextField()
    long_content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='article_images/')
    slug = models.SlugField(unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


    def get_detail_url(self):
        return reverse(
            'articles:detail',
            kwargs={
                'year': self.created_at.year,
                'month': self.created_at.month,
                'day': self.created_at.day,
                'slug': self.slug,
            })



class Comment(models.Model):
     post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
     name = models.CharField(max_length=80)
     email = models.EmailField()
     comment = models.TextField()
     created = models.DateTimeField(auto_now_add=True)



     class Meta:
         ordering = ['created']
         indexes = [
         models.Index(fields=['created']),
     ]

class CommentForm(forms.ModelForm):
     class Meta:
         model = Comment
         fields = ['name', 'email', 'comment']

     def __str__(self):
         return f'Comment by {self.name} on {self.post}'



