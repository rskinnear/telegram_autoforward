from datetime import datetime


def get_shift_from_timestamp(message_timestamp: datetime):
    """
    Fetches the shift color based on the current timestamp.
    """
    hour = message_timestamp.hour
    weekday = message_timestamp.weekday()

    if weekday in [0, 1]:  # Monday, Tuesday
        if 0 <= hour < 6:
            return "red"
        elif 6 <= hour < 14:
            return "yellow"
        elif 14 <= hour < 23:
            return "green"
        else:
            return "red"
    elif weekday in [2, 3]:  # Wednesday, Thursday
        if 0 <= hour < 7:
            return "red"
        elif 7 <= hour < 15:
            return "blue"
        elif 15 <= hour < 23:
            return "green"
        else:
            return "red"
    elif weekday == 4:  # Friday
        if 0 <= hour < 6:
            return "red"
        elif 6 <= hour < 14:
            return "yellow"
        elif 14 <= hour < 18:
            return "green"
        elif 18 <= hour < 22:
            return "blue"
        else:
            return "purple"
    elif weekday == 5:  # Saturday
        if 0 <= hour < 6:
            return "purple"
        elif 6 <= hour < 13:
            return "yellow"
        elif 13 <= hour < 22:
            return "blue"
        else:
            return "purple"
    else:  # Sunday
        if 0 <= hour < 6:
            return "purple"
        elif 6 <= hour < 13:
            return "yellow"
        elif 13 <= hour < 22:
            return "blue"
        else:
            return "red"
