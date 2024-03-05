import bleach
from datetime import timedelta
from django.utils import timezone

def sanitize_token(token):
    cleaned_token = bleach.clean(token, tags=[], attributes={})
    
    return cleaned_token

def calculate_minutes_passed(token):
    current_utc_time = timezone.now()

    time_difference = current_utc_time - token.created_at

    time_difference_with_offset = time_difference + timedelta(minutes=token.offset)

    minutes_passed = time_difference_with_offset.total_seconds() / 60

    return minutes_passed
