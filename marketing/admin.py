from django.contrib import admin

from .models import MarkettingPreference



class MarkettingPreferenceAdmin(admin.ModelAdmin):
    display_list = ['__str__', 'subscribed','updated']
    readonly_fields = ['mailchimp_subscribed', 'mailchimp_msg', 'timestamp', 'updated']
    class Meta:
        model = MarkettingPreference
        fields = [
            'user',
            'subscribed',
            'mailchimp_subscribed',
            'mailchimp_msg',
            'timestamp',
            'updated'
        ]


admin.site.register(MarkettingPreference, MarkettingPreferenceAdmin)

