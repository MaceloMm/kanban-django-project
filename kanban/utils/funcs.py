from uuid import uuid4

def get_filename(_instance, filename):
    return f'{uuid4()}.{filename.split('.')[-1]}'