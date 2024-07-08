from django.contrib import admin
from blog.models import Event, Member, User, People, Contact
from import_export  import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.


# admin.site.register(Event)
admin.site.register(Member)
@admin.register(Event)
class CustomerModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display= ('title', 'description')


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_superuser')

    search_fields = ('email',)

    list_filter = ('date_joined',)
    date_hierarchy = 'date_joined'

admin.site.register(People)
admin.site.register(Contact)