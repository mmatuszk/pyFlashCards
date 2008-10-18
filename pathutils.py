import os.path

def nativepath(path):
    if not path:
        return None

    l = path.split('\\')
    if len(l) == 1:
        return path
    else:
        new_path = ''
        for n in l:
           new_path = os.path.join(new_path, n)
        return new_path

    l = path.split('/')
    if len(l) == 1:
        return path
    else:
        new_path = ''
        for n in l:
           new_path = os.path.join(new_path, n)
        return new_path
