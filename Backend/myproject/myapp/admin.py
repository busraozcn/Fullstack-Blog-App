# admin.py
from django.contrib import admin
from .models import User, Post, Comment, Album, Photo, Todo, Address, Geo, Company
from django.contrib.auth.models import Permission

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Todo)
admin.site.register(Address)
admin.site.register(Geo)
admin.site.register(Company)
admin.site.register(Permission)
