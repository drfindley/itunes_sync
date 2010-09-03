#!/usr/bin/python

from pprint import pprint
import pickle
import os
import config
import shutil
from time import sleep
import copy
import sys

def execute(cmd):
    import subprocess
    
    proc = subprocess.Popen(cmd,shell=True,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = proc.communicate()

    stdout = output[0].strip()
    stderr = output[1].strip()

    return stdout

HOSTNAME = execute("scutil --get ComputerName")
MUSIC_DIR = config.hosts[HOSTNAME]['music_folder']
BACKUP_FOLDER = config.hosts[HOSTNAME].get('backup_folder','')
LOCK_FILE = os.path.join(MUSIC_DIR,"transfer.lock")
COMPUTERS_PICKLE = os.path.join(MUSIC_DIR,"computers.pickle")
FILE_TYPES = ['mp3','mp4','m4a']

class Computers(dict):
    def __init__(self,dict):
        super(self.__class__,self).__init__(dict)
        for hostname,computer in dict.iteritems():
            self[hostname] = Computer(hostname,computer)

    @classmethod
    def init_with_pickle(self,pickle_file):

        with open(pickle_file,'rb') as f:
            dict = pickle.load(f)

        c = Computers(dict)
        c.pickle_file = pickle_file
        return c

    def save_pickle(self):
        if not self.pickle_file:
            raise Exception("No pickle file to save to!")

        computers = {}
        for hostname,c in self.iteritems():
            computer = {}
            for folder,mfiles in c.iteritems():
                music_folder = []
                for mfile in mfiles:
                    music_folder.append((mfile.rel_path,mfile.md5))

                if music_folder:
                    computer[folder] = music_folder

            computers[hostname] = computer

        with open(self.pickle_file,'wb') as f:
            pickle.dump(computers,f)
        #pprint(computers)

    def get_md5s(self,exclude=None):
        md5_set = set()
        for host,comp in self.iteritems():
            if host == exclude:
                continue
            [md5_set.add(music_file.md5) for folders in comp.values() for music_file in folders]
        return md5_set

class Computer(dict):
    def __init__(self,hostname,dict):
        super(self.__class__,self).__init__(dict)

        self.hostname = hostname
        for music_folder,music_files in dict.iteritems():
            self[music_folder] = MusicFolder(music_folder,music_files)

    def __repr__(self):
        return super(self.__class__,self).__repr__()

class MusicFolder(list):
    def __init__(self,folder,files):
        self.name = folder
        
        files.sort()
        files.reverse()

        for music_file,md5 in files:
            self.append(MusicFile(music_file,md5,self.name))

    def __repr__(self):
        return super(self.__class__,self).__repr__()

    def delete(self,music_file,safe_files):
        if music_file.md5 not in safe_files and music_file.exists():
            print "REMOVE: %s" % music_file.abs_path
            os.remove(music_file.abs_path)
        self.remove(music_file)

        length = music_file.abs_path.find(self.name) + len(self.name) + 1
        directories = os.path.dirname(music_file.abs_path[length:]).split('/')
        base_path = music_file.abs_path[:length]

        while directories:
            path = '/'.join(directories)
            abs_path = base_path + path
            directories.pop()

            if os.path.exists(abs_path):
                if not os.listdir(abs_path):
                    print 'REMOVE: ',abs_path
                    os.rmdir(abs_path)

    def add_to_itunes(self,playlist=None):
        if not playlist: playlist = self.name

        #TODO If the playlist doesn't exist, create it
        abs_path = os.path.join(MUSIC_DIR,self.name)

        add_to_playlist = "osascript -e 'tell application \"iTunes\" to add POSIX file \"%s\" to playlist \"%s\"'" % (abs_path,playlist)
        print add_to_playlist
        execute(add_to_playlist)
        sleep(2)


class MusicFile:
    def __init__(self,music_file,md5,folder):
        self.md5 = md5
        self.rel_path = music_file
        self.abs_path = os.path.join(MUSIC_DIR, music_file)
        self.extension = os.path.splitext(music_file)[1][1:].lower()
        self.folder = folder

    def exists(self):
        return os.path.exists(self.abs_path)

    def verify(self):
        if not self.exists():
            print "File %s doesn't exist" % self.abs_path
            return False

        from hashlib import md5
        with open(self.abs_path,'rb') as f:
            hash = md5(f.read()).hexdigest()

        if hash != self.md5:
            print "File %s doesn't match md5's" % self.abs_path
            return False

        return True

    def add_to_itunes(self,playlist=None):
        if not playlist: playlist = self.folder

        #TODO If the playlist doesn't exist, create it

        add_to_playlist = "osascript -e 'tell application \"iTunes\" to add POSIX file \"%s\" to playlist \"%s\"'" % (self.abs_path,playlist)
        print add_to_playlist
        execute(add_to_playlist)
        sleep(2)

    def backup(self,backup_folder):
        backup_file = os.path.join(backup_folder,self.rel_path)
        directory = os.path.dirname(backup_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy(self.abs_path,backup_file)

    def __repr__(self):
        return "('%s','%s')" % (self.rel_path,self.md5)

# Aquire lock file
sleep(60)
while os.path.exists(LOCK_FILE):
    print "Lock already aquired"
    sleep(60)
open(LOCK_FILE, 'w').close()

computers = Computers.init_with_pickle(COMPUTERS_PICKLE)

# Make sure our computer exists
computer = computers.get(HOSTNAME,'')
if not computer:
    print HOSTNAME
    print "System Exit"
    print "Removing lock file"
    os.remove(LOCK_FILE)
    sys.exit(0)

folders_to_pop = []
removed_md5s = []
music_directories = {}
safe_files = computers.get_md5s(exclude=HOSTNAME)

computers.save_pickle()

for music_folder in computer.values():
    music_files = list(music_folder)
    music_folder.add_to_itunes()

    # check file
    while music_files:
        music_file = music_files.pop()
        print music_file.rel_path

        if music_file.verify():
            if music_file.extension not in FILE_TYPES:
                print "File: %s" % music_file

            if BACKUP_FOLDER:
                music_file.backup(BACKUP_FOLDER)

        music_folder.delete(music_file,safe_files)

computers.save_pickle()

sleep(60)
os.remove(LOCK_FILE)
sleep(10)
