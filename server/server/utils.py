from django.utils.timesince import timesince
from django.utils.timezone import now
from datetime import timedelta

def get_readable_time_since(time_to_compare):
    """
    Returns a human-readable string:
    - 'X ago' if in the past
    - 'X left' if in the future
    """
    delta = now() - time_to_compare

    if delta.total_seconds() >= 0:
        # past
        if delta < timedelta(minutes=1):
            return "just now"
        elif delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta < timedelta(days=7):
            days = delta.days
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            return f"{timesince(time_to_compare)} ago"
    else:
        # future
        delta = -delta  # make positive
        if delta < timedelta(minutes=1):
            return "less than a minute left"
        elif delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} left"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} left"
        elif delta < timedelta(days=7):
            days = delta.days
            return f"{days} day{'s' if days != 1 else ''} left"
        else:
            return f"{timesince(now(), time_to_compare)} left"
