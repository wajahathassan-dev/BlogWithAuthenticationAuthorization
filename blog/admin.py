from django.contrib import admin

# model
from blog.models import BlogPost

admin.site.register([BlogPost])
