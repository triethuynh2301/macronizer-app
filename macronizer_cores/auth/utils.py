from flask import g, session
from macronizer_cores import CURRENT_USER


def remove_user_from_session():
    '''
    if currently logged in -> log out
    '''

    if g.user:
        # remove key from session
        del session[CURRENT_USER]