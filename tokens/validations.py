def validate_input(data):
    errors = []

    # Day Validation
    day = data.get('day')
    if day is not None:
        try:
            day = int(day)
            if day < 1 or day > 31:
                errors.append("Day should be between 1 and 31.")
        except ValueError:
            errors.append("Day should be an integer.")

    # Hours Validation
    hours = data.get('hours')
    if hours is not None:
        try:
            hours = int(hours)
            if hours < 0 or hours > 23:
                errors.append("Hours should be between 0 and 23.")
        except ValueError:
            errors.append("Hours should be an integer.")

    # Minutes Validation
    minutes = data.get('minutes')
    if minutes is not None:
        try:
            minutes = int(minutes)
            if minutes < 0 or minutes > 59:
                errors.append("Minutes should be between 0 and 59.")
        except ValueError:
            errors.append("Minutes should be an integer.")

    # Seconds Validation
    seconds = data.get('seconds')
    if seconds is not None:
        try:
            seconds = int(seconds)
            if seconds < 0 or seconds > 59:
                errors.append("Seconds should be between 0 and 59.")
        except ValueError:
            errors.append("Seconds should be an integer.")

    return errors