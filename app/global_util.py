from flask import redirect
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from re import sub


def user_has_role(user, required_roles):
    """A decorator for views that not only need to check if the user is authenticated
    but also if the user has the required role to see the view. It takes flask's
    current_user as an argument and then a tuple of required_roles. If the user
    does not have the required role they are directed to a page that is suitable for
    the role they have. So someone with the role of user will be directed to
    /user/home."""

    def decorator(func):

        wraps(func)

        def the_last_func(*args, **kwargs):

            for role in user.roles:

                if role not in required_roles:
                    return redirect("/" + role + "/home")

            return func(*args, **kwargs)

        return the_last_func

    return decorator


def strip_text(text: list, turnto_int=False, toStr=False):
    """Takes a list of tag numbers that along with additional chrs.
    These additional chrs are strip, the tag number is converted to an 
    integer and appended to a list which is then returned."""

    tagnum_list = []

    wordInput = ""

    if turnto_int:

        for char in text:
            
            stripped_text = int(sub("[() {}, <> ]", "", char))

            tagnum_list.append(stripped_text)

    if toStr:

        for char in text:

            stripped_text = sub("[() {}, <> ]", "", char)

            wordInput += stripped_text

        return wordInput

            
    else:

        for char in text:

            stripped_text = sub("[() {}, <> ]", "", char)

            tagnum_list.append(stripped_text)

    return tagnum_list




