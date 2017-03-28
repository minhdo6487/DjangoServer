from django.contrib import admin

from .models import (Question,
                     UrlNav,
                     SubUrlNav,
                     Restaurant,
                     BlogPost
                     )
admin.site.register(Question)
admin.site.register(UrlNav)
admin.site.register(SubUrlNav)
admin.site.register(Restaurant)
admin.site.register(BlogPost)
