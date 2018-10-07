import os

for parent, dirnames, filenames in os.walk(r"C:\Users\John\Desktop\New folder"):
    for fn in filenames:
        if fn == 'cities.xml':
            os.remove(os.path.join(parent, fn))