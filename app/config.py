# CONFIG

hosts = {
    'cuttooth':{
        'base_folder':'/Volumes/data/adam/Dropbox/Music Transfer',
        'monitor_folders': ['Amazon MP3', 'Emusic', 'other', 'iTunes [Exclude Fasttrack]', 'iTunes [Exclude Melatonin]'],
        'backup_folders': [],
        'itunes_folder': '',
    },
    'fasttrack':{
        'base_folder':'/Volumes/data/adam/Dropbox/Dropbox/Music Transfer',
        'monitor_folders': ['Amazon MP3', 'Emusic', 'other', 'iTunes [Exclude Cuttooth]', 'iTunes [Exclude Melatonin]'],
        'backup_folders': [],
        'itunes_folder': '',
    },
    'melatonin':{
        'base_folder':'/Users/adam/Dropbox/Music Transfer',
        'monitor_folders': ['Amazon MP3', 'Emusic', 'other', 'iTunes [Exclude Cuttooth]', 'iTunes [Exclude Fasttrack]'],
        'backup_folders': ['/Volumes/Drobo/Music [Lossy]'],
        'itunes_folder': '/Volumes/iTunes/iTunes Test/iTunes Media/Automatically Add to iTunes',
    },
}

monitor = {
    'monitor_base_folder': 'Downloads',
    'monitor_lock':'monitor.lock'
}

transfer = {
    'transfer_base_folder': 'Transfer',
}
