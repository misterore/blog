import os


class Config(object):
    SECRET_KEY = os. environ.get('SECRET _KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = '/Users/mister_ore/Documents/blog/app/static/images'
    MAX_CONTENT_LENGTH = 100 * 2000 * 2000
