import sys
import os
from os import listdir
from os.path import isfile, join
import subprocess

def exec_cmd(cmd:str):
    p = subprocess.run(cmd, shell = True, executable="/bin/bash")
    if p.returncode != 0:
        print(cmd, p.args)

# constants
OUTPUT_DIR = sys.argv[2]
TEMP_DIR = OUTPUT_DIR
FILE_NAME = "urls.txt" 
ERR_FILE_NAME = "errors.log"
ERR_FILE = "%s/%s" % (OUTPUT_DIR, ERR_FILE_NAME)
DEL = "_##_"

# File check
if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
    sys.exit('Please create a file "urls.txt" in this directoty and add urls in separate lines that you want downloaded.')

# Set flags
flags = [
    '--lyrics genius', 
    '--preload', 
    '--restrict ascii',
    '--scan-for-songs --overwrite skip', 
    '--add-unavailable',
    '--max-retries 100',
    '--audio youtube-music youtube soundcloud bandcamp piped slider-kz',
    '--save-errors %s' % (ERR_FILE),
    '--output "%s/%s{artist}%s{album}%s{disc-number}%s{track-number}%s{title}"' % (TEMP_DIR, DEL, DEL, DEL, DEL, DEL)
]

output_fmt = sys.argv[1]
if output_fmt not in ['mp3','flac','ogg','opus','m4a','wav']:
    sys.exit('Please select a proper output format {mp3,flac,ogg,opus,m4a,wav}')
flags.append("--format %s" % (output_fmt))

# Run cmd
exec_cmd("mkdir -p %s; mkdir -p %s" % (OUTPUT_DIR, TEMP_DIR))
    
cmd = "spotdl download $(cat %s) %s" % (FILE_NAME, " ".join(flags))
exec_cmd(cmd)

if os.stat(ERR_FILE).st_size != 0: # log error
    with open(ERR_FILE, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("make run: There were some errors getting some tracks. Try running the script again; if not, try manually download each track." + '\n\n' + content)

# Organize music into the directories
music = {}
for f in listdir('%s' %(TEMP_DIR)):
    if not f.startswith(DEL):
        continue
    
    # get metadata from file name
    m = f.replace('"', '').split(DEL)[1:]
    md = {
        "artist": m[0], "album": m[1], "disc_number": m[2], 
        "track_num": m[3], "track_name": m[4], "file_name": f
        }
    if md["disc_number"].isnumeric():
        md["disc_number"] = int(md["disc_number"])
    else:
        md["disc_number"] = 1
    
    if md["disc_number"] > 1:
        md["album"] = '%s - Disc %s' % (md["album"], str(md["disc_number"]))
    
    # create artist and/or album
    if md["artist"] not in music:
        music[md["artist"]] = {}
    if md["album"] not in music[md["artist"]]:
        music[md["artist"]][md["album"]] = {}
    
    # store
    tn = '%s %s' % (md["track_num"], md["track_name"])
    music[md["artist"]][md["album"]][tn] = md["file_name"]

# Check if inclusion of '- Dis1' is needed
for artist in music:
    for album in music[artist]:
        d_name = '%s - Disc 1' % (md["album"])
        for ab in music[md["artist"]]: # if other disc from album already exist
            if "- Disc" in ab:
                disc1_data = music[md["artist"]][md["album"]]
                del music[md["artist"]][md["album"]]
                music[md["artist"]][d_name] = disc1_data
        
# Move to music folder
for artist in music:
    exec_cmd('mkdir -p "%s/%s"' % (OUTPUT_DIR, artist))
    for album in music[artist]:
        exec_cmd('mkdir -p "%s/%s/%s"' % (OUTPUT_DIR, artist, album))
        for song, f_name in music[artist][album].items():
            new_path = '"%s/%s/%s/%s"' % (OUTPUT_DIR, artist, album, song)
            curr_path = '"%s/%s"' % (TEMP_DIR, f_name)
            exec_cmd("mv %s %s" % (curr_path, new_path))

# Clean
# for artist in music:
#     artist_path = '"%s/%s"' % (OUTPUT_DIR, artist)
#     print(artist_path)
#     if len(os.listdir(artist_path)) == 0:  
#         exec_cmd("rm -rf %s" % (artist_path))
#     else:    
#         for album in music[artist]:
#             album_path = '"%s/%s/%s"' % (OUTPUT_DIR, artist, album)
#             if len(os.listdir(album_path)) == 0:  
#                 exec_cmd("rm -rf %s" % (album_path))

if TEMP_DIR != OUTPUT_DIR:
    exec_cmd("rm -rf %s" % (TEMP_DIR))