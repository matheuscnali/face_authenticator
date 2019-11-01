import PIL.Image, PIL.ImageTk

def authenticate(photo_f, photo_s):




    result = {}

    user = 'Matheus Carvalho Nali'
    result['text'] = 'Acesso garantido, %s.' % (user)
    result['im'] = 'check'

    return result