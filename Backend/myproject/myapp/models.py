from django.db import models

class Geo(models.Model):
    lat = models.CharField(max_length=500, blank=True, null=True)
    lng = models.CharField(max_length=500, blank=True, null=True)

class Address(models.Model):
    street = models.CharField(max_length=200, blank=True, null=True)
    suite = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    geo = models.OneToOneField(Geo, on_delete=models.CASCADE, related_name='address', blank=True, null=True)

class Company(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    catchPhrase = models.CharField(max_length=255, default="Centralized empowering task-force", blank=True, null=True)
    bs = models.CharField(max_length=255, default="target end-to-end models", blank=True, null=True)

class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='user', blank=True, null=True)

class Post(models.Model):
    userId = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()

class Comment(models.Model):
    postId = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    email = models.EmailField()
    body = models.TextField()

class Album(models.Model):
    userId = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    thumbnailUrl = models.CharField(max_length=200)

class Todo(models.Model):
    userId = models.ForeignKey(User, related_name='todos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField()
