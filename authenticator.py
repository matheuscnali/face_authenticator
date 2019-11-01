import PIL.Image, PIL.ImageTk

def authenticate(photo_f, photo_s):

    result = {}

    user = 'User'
    result['text'] = 'Acess granted, %s.' % (user)
    result['im'] = 'check'

    return result