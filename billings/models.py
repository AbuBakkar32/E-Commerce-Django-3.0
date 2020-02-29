from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.urls import reverse

from accounts.models import GuestEmail

import stripe

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        obj = None
        created = False
        guest_user_id = request.session.get("guest_user_id")
        user = request.user
        if user.is_authenticated:
            "logged in user checkout; rememver payment stuff"
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)

        elif guest_user_id is not None:
            "guest  user checkout; auto reloads payment stuff"
            guest_user_email = GuestEmail.objects.get(id=guest_user_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_user_email.email
            )
        else:
            pass

        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email
    
    def get_payment_method(self):
        return reverse('payment-method')

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    @property
    def has_card(self): 
        card_qs = self.get_cards()
        return card_qs.exists()

    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
                return default_cards.first()
        return None
    
    def set_cards_inactive(self):
        card_qs = self.get_cards()
        card_qs.update(active=False)
        return card_qs.filter(active=True).count()


def customer_id_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(email=instance.email)
        instance.customer_id = customer.id

pre_save.connect(customer_id_receiver, sender=BillingProfile)


def user_create_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_create_receiver, sender=settings.AUTH_USER_MODEL)


class CardManager(models.Manager):
    
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)
    
    def add_new(self, billing_profile, token):
        if token:
            stripe_card = stripe.Customer.create_source(
                billing_profile.customer_id, source=token
            )
            new_card = self.model(
                billing_profile=billing_profile,
                stripe_id=stripe_card.id,
                brand=stripe_card.brand,
                country=stripe_card.country,
                exp_month=stripe_card.exp_month,
                exp_year=stripe_card.exp_year,
                last4=stripe_card.last4,
            )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    brand                   = models.CharField(max_length=120, blank=True, null=True)
    country                 = models.CharField(max_length=120, null=True, blank=True)
    exp_month               = models.IntegerField(null=True, blank=True)
    exp_year                = models.IntegerField(null=True, blank=True)
    last4                   = models.CharField(max_length=4, null=True, blank=True)
    default                 = models.BooleanField(default=True)
    active                  = models.BooleanField(default=True)
    timestamp               = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)
    
    
def new_card_post_save_receiver(instance, sender, created, *args, **kwargs):
    if instance.default:
        qs = Card.objects.filter(billing_profile = instance.billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)

post_save.connect(new_card_post_save_receiver, sender=Card)


class ChargeManger(models.Manager):
    def do(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No card Available"

        c = stripe.Charge.create(
            amount=int(order_obj.total * 100),
            currency="bdt",
            customer=billing_profile.customer_id,
            source=card_obj.stripe_id,
            metadata={"order_id": order_obj.order_id},
        )

        new_carge_obj = self.model(
            billing_profile=billing_profile,
            stripe_id=c.id,
            paid=c.paid,
            refunded=c.refunded,
            outcome=c.outcome,
            outcome_type=c.outcome["type"],
            seller_message=c.outcome.get("seller_message"),
            risk_level=c.outcome.get("risk_level"),
        )
        new_carge_obj.save()

        return new_carge_obj.paid, new_carge_obj.seller_message


class Charge(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    paid                    = models.BooleanField(default=False)
    refunded                = models.BooleanField(default=False)
    outcome                 = models.TextField(null=True, blank=True)
    outcome_type            = models.CharField(max_length=120, null=True, blank=True)
    seller_message          = models.CharField(max_length=120, null=True, blank=True)
    risk_level              = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManger()

