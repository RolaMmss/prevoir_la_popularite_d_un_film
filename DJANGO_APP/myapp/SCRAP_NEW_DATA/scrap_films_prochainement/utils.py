from datetime import datetime
import locale


def convert_to_minutes(time: str) -> int or None:
    '''
    Convert the duration of a movie to minutes.

    Args:
        time (str): The duration of a movie in the format 'h min' or 'h'.

    Returns:
        [int, None]: The duration of the movie in minutes or None if the duration is invalid.
    '''
    if time:
        # Remove any leading/trailing whitespace or newline characters
        time = time.strip()
        
        if 'h' in time and 'min' in time:
            hours, minutes = time.split('h ')
            minutes = minutes.replace('min', '').strip()
            duration = int(hours) * 60 + int(minutes)
        elif 'h' in time:
            hours = time.replace('h', '').strip()
            duration = int(hours) * 60
        elif 'min' in time:
            minutes = time.replace('min', '').strip()
            duration = int(minutes)
        else:
            duration = None
    else:
        duration = None
        
    return duration


def convert_to_dd_mm_aaaa(date_str):
    if date_str:
        try:
            # Set the locale manually for the script
            locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
            date_obj = datetime.strptime(date_str, '%d %B %Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
            return formatted_date
        except ValueError:
            return None
    return None


