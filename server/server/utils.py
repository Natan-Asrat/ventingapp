

from django.utils.timesince import timesince
from django.utils.timezone import now
from datetime import timedelta
def get_readable_time_since(time_to_compare):
    """
    Returns a human-readable 'time ago' string without checking strings.
    """
    delta = now() - time_to_compare

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
        # fallback to timesince for longer periods
        return f"{timesince(time_to_compare)} ago"