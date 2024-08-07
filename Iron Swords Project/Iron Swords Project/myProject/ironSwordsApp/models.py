from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
# ironSwordsApp/models.py

class Hero(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    hometown = models.CharField(max_length=100)
    country_of_birth = models.CharField(max_length=100)
    hero_story = models.TextField()
    image = models.ImageField(upload_to='heroes_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class KibbutzStory(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class NovaPartyTestimony(models.Model):
    owner = models.CharField(max_length=100)
    story = models.TextField()


    def __str__(self):
        return self.owner
    
class Testimonial(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.TextField()

    def __str__(self):
        return self.author.username
    
