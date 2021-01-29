from django.contrib import admin
from .models import Profile
from .models import Website
from .models import Comment
from .models import Founder
from .models import Industry
from .models import AreaServed
from .models import WebsiteLikes
from .models import WebsiteDislikes
from .models import CommentLikes
from .models import CommentDislike


# Register your models here.

# Website model
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('website_domain_name', 'name', 'writen_by')
    list_filter = ('industry', 'areaServed')


# Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'website_id', 'comment_id', 'reply')

    def get_username(self, obj):
        return obj.user_id.user.username
    get_username.short_description = 'User'


# Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_last_name', 'get_first_name', 'get_email')

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'User'

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'Last Name'

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'First Name'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'


# admin.site.register(Profile)
# admin.site.register(Website)
# admin.site.register(Comment)
admin.site.register(Industry)
admin.site.register(AreaServed)
admin.site.register(Founder)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.register(WebsiteLikes)
admin.site.register(WebsiteDislikes)
admin.site.register(CommentLikes)
admin.site.register(CommentDislike)
