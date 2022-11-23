from django.contrib import admin
from .models import Author, Follower
from django.contrib import messages
from django.utils.translation import ngettext



# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/actions/

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['displayName', 'isAuthorized']
    ordering = ['displayName']
    actions = ['set_as_authorized']


    @admin.action(description='Set selected authors to authorized')
    def set_as_authorized(self, request, queryset):

        previously_authorized = len(queryset.filter(isAuthorized=True))
        updated = queryset.update(isAuthorized=True)
        num_updated = updated - previously_authorized
        if num_updated:
            self.message_user(request, ngettext(
                    '%d authors were successfully authorized.',
                    '%d authors were successfully authorized.',
                    num_updated,
                ) % num_updated, messages.SUCCESS)
        if previously_authorized:
            self.message_user(request, ngettext(
                    '%d authors are already authorized.',
                    '%d authors are already authorized.',
                    previously_authorized,
                ) % previously_authorized, messages.WARNING)
        

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Follower)
