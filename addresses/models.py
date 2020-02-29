from django.db import models

from billings.models import BillingProfile


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    # ADDRESS_TYPE = (
    #     ('billing', 'Billing'),
    #     ('shipping', 'Shippinpg')
    # )
    # address_type    = models.CharField(max_length=20, choices=ADDRESS_TYPE)
    full_name       = models.CharField(max_length=120)
    mobile_number   = models.IntegerField()
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, blank=True)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120)
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)
    
    
    def __str__(self):
        return str(self.billing_profile)
    
    def get_address(self):
        return f"{self.address_line_1}, {self.city}, {self.country}, {self.state}, {self.postal_code}"
