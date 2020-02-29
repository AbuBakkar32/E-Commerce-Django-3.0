import hashlib
import re
import json
import requests
from django.conf import settings


MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)



def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return


def get_subscriber_hash(member_email):
    '''
    This makes a email hash which is required by the Mailchimp API
    '''
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()


class Mailchimp(object):
    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url  = 'https://{dc}.api.mailchimp.com/3.0'.format(
                                    dc=MAILCHIMP_DATA_CENTER
                                )
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(
                                    api_url = self.api_url,
                                    list_id=self.list_id
                        )
    
    def change_subscription_status(self, email, status):
        subscriber_hash     = get_subscriber_hash(email)
        members_endpoint       = self.get_members_endpoint()
        endpoint            = "{members_endpoint}/{sub_hash}".format(
                                members_endpoint=members_endpoint, 
                                sub_hash=subscriber_hash
                                )
        data                = {
                                "status": self.check_valid_status(status)
                            }
        r                   = requests.put(endpoint, 
                                auth=("", MAILCHIMP_API_KEY), 
                                data=json.dumps(data)
                                )
        return r.status_code, r.json()
        
    def check_subscription_status(self, email):
        subscriber_hash     = get_subscriber_hash(email)
        members_endpoint       = self.get_members_endpoint()
        endpoint            = "{members_endpoint}/{sub_hash}".format(
                                members_endpoint=members_endpoint, 
                                sub_hash=subscriber_hash
                                )
        r                   = requests.get(endpoint, 
                                auth=("", MAILCHIMP_API_KEY)
                                )
        return r.status_code, r.json() 
    
    def check_valid_status(self, status):
        choices = ['subscribed','unsubscribed', 'cleaned', 'pending']
        if status not in choices:
            raise ValueError("Not a valid choice")
        return status  
    
    def get_members_endpoint(self):
        endpoint = '{list_endpoint}/members'.format(
                                    list_endpoint=self.list_endpoint)
        return endpoint
    
    def add_email(self, email):
        check_email(email)
        endpoint = self.get_members_endpoint()
        data = { 
                "email_address": email, 
                "status": "subscribed",
                "merge_fields": {}
                }
        r = requests.post(endpoint, 
                    auth=("", MAILCHIMP_API_KEY), 
                    data=json.dumps(data)
                    )
        return self.change_subscription_status(email, status='subscribed')
    
    
    def unsubscribe(self, email):
        return self.change_subscription_status(email, status='unsubscribed') 
    
    
    def subscribe(self, email):
        return self.change_subscription_status(email, status='subscribed') 
    
    def pending(self, email):
        return self.change_subscription_status(email, status='unsubscribed') 


    


