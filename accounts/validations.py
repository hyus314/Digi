import re

username_regex = r'^[a-z0-9_-]{3,16}$'
name_regex = r'^[a-zA-Z]+$'
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def validate_username(username):
    if not re.match(username_regex, username):
        return False
    else:
        return True
    

def validate_names(first_name, last_name):
    if not re.match(name_regex, first_name) or not re.match(name_regex, last_name):
        return False
    else:
        return True


def validate_email(email):
    if not re.match(email_regex, email):
        return False
    else:
        return True


def validate_password(password, confirmation):
    if len(password) < 8 or len(password) > 20:
        print('1')
        return False
    if not has_uppercase(password):
        print('2')
        return False
    if not has_numeric(password):
        print('3')
        return False
    if not password.isalnum():
        print('4')
        return False
    if password != confirmation:
        print('5')
        return False
    
    return True



def has_uppercase(s):
    return any(char.isupper() for char in s)

def has_numeric(s):
    return any(char.isdigit() for char in s)