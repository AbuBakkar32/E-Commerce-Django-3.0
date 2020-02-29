from django.contrib import admin

from django.contrib.auth import get_user_model

from .models import GuestEmail, UserProfile, EmailActivation

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeform, UserProfileForm

User = get_user_model()



class UserAdmin(BaseUserAdmin):
    # search_fields = ['email']
    form = UserAdminChangeform
    add_form = UserAdminCreationForm
    
    list_display = ('email', 'admin')
    list_filter = ('admin', 'staff','is_active')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permission', {'fields': ('admin', 'staff', 'is_active')})
    )
    
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )
    
    search_fields = ('email','full_name')
    ordering = ('email',)
    filter_horizontal = ()
    
    
        
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)







class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmail
        
admin.site.register(GuestEmail, GuestEmailAdmin)


admin.site.register(UserProfile)

admin.site.register(EmailActivation)


