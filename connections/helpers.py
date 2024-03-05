import bleach
from datetime import timedelta
from django.utils import timezone

def sanitize_token(token):
    cleaned_token = bleach.clean(token, tags=[], attributes={})
    
    return cleaned_token

def calculate_minutes_passed(token):
    current_utc_time = timezone.now()

    time_token_created = token.created_at + timedelta(minutes=token.offset)
    
    if current_utc_time >= time_token_created + timezone.timedelta(minutes=15):
        return True
    
    return False
    breakpoint()
    
