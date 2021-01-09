from django.contrib import admin
from .models import User
from .models import Website
from .models import Comment
from .models import Founder
from .models import Industry
from .models import AreaServed


# Register your models here.
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('website_domain_name', 'name', 'writen_by')
    list_filter = ('industry', 'areaServed')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'website_id', 'comment_id', 'reply')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email')


# admin.site.register(User)
# admin.site.register(Website)
# admin.site.register(Comment)
admin.site.register(Industry)
admin.site.register(AreaServed)
admin.site.register(Founder)
admin.site.register(User, UserAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Comment, CommentAdmin)
