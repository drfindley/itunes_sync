import os

name = 'other'
abs_path = '/Users/adam/Dropbox/Music Transfer/other/Death Cab For Cutie/The Open Door EP/01 - Little Bribes.mp3'
length = abs_path.find(name) # + len(name) + 1
directories = os.path.dirname(abs_path[length:]).split('/')
base_path = abs_path[:length]

while directories:
    path = '/'.join(directories)
    abs_path = base_path + path
    directories.pop()

    if os.path.exists(abs_path):
        if not os.listdir(abs_path):
            print 'Remove: ',abs_path
            os.rmdir(abs_path)

