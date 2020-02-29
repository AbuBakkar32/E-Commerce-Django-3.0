from django.dispatch import Signal

user_login_signal = Signal(providing_args=['instance', 'request'])



