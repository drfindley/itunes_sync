# CONFIG

hosts = {
    'cuttooth':{
        'base_folder':'/Users/adam/Dropbox/Music Transfer',
        'monitor_folders': ['Amazon MP3', 'Emusic', 'other', 'iTunes [Exclude cuttooth]', 'iTunes [Exclude fasttrack]', 'iTunes [Exclude melatonin]'],
        'backup_folders': [],
        'itunes_folder': '/Users/adam/Music/iTunes/iTunes Media/Automatically Add to iTunes',
    },
    'fasttrack':{
        'base_folder':'/Users/adam/Dropbox/Music Transfer',
        'monitor_folders': ['Amazon MP3', 'Emusic', 'other', 'iTunes [Exclude cuttooth]', 'iTunes [Exclude fasttrack]', 'iTunes [Exclude melatonin]'],
        'backup_folders': [],
        'itunes_folder': '/Users/adam/Music/iTunes/iTunes Music/Automatically Add to iTunes',
    },
    'melatonin':{
        'base_folder':'/Users/adam/Dropbox/Music Transfer',
        'monitor_folders': ['Amazon MP3', 'Emusic', 'other', 'iTunes [Exclude cuttooth]', 'iTunes [Exclude fasttrack]', 'iTunes [Exclude melatonin]'],
        'backup_folders': ['/Volumes/Drobo/Music [Lossy]'],
        'itunes_folder': '/Users/adam/Music/iTunes/iTunes Media/Automatically Add to iTunes',
    },
}

monitor = {
    'monitor_base_folder': 'Downloads',
    'monitor_lock':'monitor.lock'
}

transfer = {
    'transfer_base_folder': 'Transfer',
}
