from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from django.contrib.sessions.models import Session 
from django.db.models.signals import pre_save, post_save

from accounts.signals import user_login_signal
from .signals import object_viewed_signal
from .utils import get_client_ip

User = get_user_model()



class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address      = models.CharField(max_length=220, blank=True, null=True)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s viewed on %s"%(self.content_object, self.timestamp)
    
    class Meta:
        ordering = ["-timestamp"]
        verbose_name = 'Object viewd'
        verbose_name_plural = 'Objects viewd'
    


    
    
    
def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    new_view_obj = ObjectViewed.objects.create(
        user = request.user,
        content_type = c_type,
        object_id = instance.id,
        ip_address = get_client_ip(request),
    )
object_viewed_signal.connect(object_viewed_receiver)






class UserSession(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address      = models.CharField(max_length=220, blank=True, null=True)
    session_key     = models.CharField(max_length=100, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    ended           = models.BooleanField(default=False)
    
    
    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.acitive = False
            self.ended = True 
            self.save()
        except:
            pass 
        return self.ended, self.active


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user,ended=False, active=False).exclude(id=instance.id)
        print(qs)
        for i in qs:
            print(i)
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()
            
post_save.connect(post_save_session_receiver, sender=UserSession)




def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    session_key = request.session.session_key
    ip_address = get_client_ip(request)
    user = instance
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )
    
user_login_signal.connect(user_logged_in_receiver)