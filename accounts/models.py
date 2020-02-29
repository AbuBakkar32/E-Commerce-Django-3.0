from django.conf import settings
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

from django.db.models.signals import post_save, pre_save

from django.core.mail import send_mail
from django.template.loader import get_template

from ecommerce.utils import unique_key_generator

from datetime import timedelta
from django.utils import timezone
from django.urls import reverse 



# send_mail(subject, message, from_email, recipient_list, html_message)



class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
        )
        
        user_obj.set_password(password)
        user_obj.staff = is_staff 
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self, email, full_name, password):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
        )
        
        return user
    
    def create_superuser(self, email, full_name, password):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        
        return user



class User(AbstractBaseUser):
    email           = models.EmailField(max_length=255, unique=True, help_text="i. Keep an unique email.")
    full_name       = models.CharField(max_length=250)
    # active          = models.BooleanField(default=True)
    is_active       = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False)
    admin           = models.BooleanField(default=False)
    timestamp       = models.DateTimeField(auto_now_add=True)
     
    USERNAME_FIELD = "email" 
    
    # USERNAME_FIELD and password are by default REQUIRED_FIELDS
    REQUIRED_FIELDS = ['full_name'] # [full_name]
    
    objects = UserManager()
    
    def __str__(self): 
        return self.email 
    
    # def mobile_number(self):
    #     return self.mobile_number
    
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email
    
    def get_short_name(self):
        return self.email  
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff  
    
    @property
    def is_admin(self):
        return self.admin 
    
    # @property
    # def is_active(self):
    #     return self.active  
    



# send email to register user 

class EmailActivationQueryset(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=7)
        end_range = now
        return self.filter(
            activated=False,
            forced_expired=False
        ).filter(
            timestamp__gt=start_range,
            timestamp__lte=end_range
        )



class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQueryset(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()



class EmailActivation(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    email           = models.EmailField()
    key             = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=7)
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)


    objects = EmailActivationManager()


    def __str__(self):
        return self.email 

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True 
        return False

    def activate(self):
        if self.can_activate():
            user = self.user 
            user.is_active = True 
            user.save()
            self.activated = True 
            self.save()
            return True 
        return False


    def regenarate(self):
        self.key = None 
        self.save()
        if self.key is not None:
            return True 
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, "BASE_URL")
                key_path = reverse("accounts:email-activation", kwargs={"key":self.key})
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email 
                }
                txt_ = get_template("registration/email/verify.txt").render(context)
                html_ = get_template("registration/email/verify.html").render(context)

                subject = "1-Click Email Varification"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list  = [self.email]
                
                sent_mail = send_mail(
                                subject,
                                txt_,
                                from_email,
                                recipient_list,
                                html_message=html_,
                                fail_silently=False
                        )
                return sent_mail
        return False


def pre_save_key_receiver(instance, sender, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_key_receiver, sender=EmailActivation)


def post_save_user_create_receiver(instance, sender, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver, sender=User)



class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'others'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="profile/", blank=True , null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.email



def user_profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = UserProfile.objects.create(user=instance)

post_save.connect(user_profile_receiver, sender=User)


def profile_save_receiver(sender, instance, *args, **kwargs):
    instance.userprofile.save()

post_save.connect(profile_save_receiver, sender=User)

