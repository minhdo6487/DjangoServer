from django.contrib import admin

from .models import Question, UrlNav, SubUrlNav

admin.site.register(Question)
admin.site.register(UrlNav)
admin.site.register(SubUrlNav)