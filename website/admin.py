from django.contrib import admin
from .models import Profile
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


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user__username', 'user__last_name', 'user__first_name', 'user__email')


admin.site.register(Profile)
# admin.site.register(Website)
# admin.site.register(Comment)
admin.site.register(Industry)
admin.site.register(AreaServed)
admin.site.register(Founder)
# admin.site.register(Profile, ProfileAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Comment, CommentAdmin)
