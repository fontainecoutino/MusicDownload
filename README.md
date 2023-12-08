# MusicDownload
Script to download music from Spotify

## About The Project 

Here is a script that downloads music from Spotify. Due to legal reasons, this script is for personal use only and I will not monetize anything.

<!-- GETTING STARTED -->
## Getting Started

### Mac
Ensure all prerequisites are met.

#### Prerequisites
Install [python3](https://www.python.org/downloads/) on your computer.
 

#### Installation

1.  Clone the repo
   ```sh
   git clone https://github.com/fontainecoutino/MusicDownload.git
   ```
2. Install dependencies
   ```sh
   make setup
   ```

<!-- USAGE EXAMPLES -->
## Usage

### Mac
To run the script, first make sure you add the spotify links in the `urls.txt` file. One link per line. 
* Default download
    ```sh
    make run
    ```
    By default, the script downloads the music in a .mp3 format.
* Custom download with output path
    ```sh
    make run FORMAT={mp3,flac,ogg,opus,m4a,wav} OUT="filepath"
    ```
#### Example `urls.txt`
Here you can add individual tracks, albums, playlist, artist.
```txt
https://open.spotify.com/track/3BQHpFgAp4l80e1XslIjNI?si=1694ec4cd9b64747
https://open.spotify.com/album/3KzAvEXcqJKBF97HrXwlgf?si=kBwTQYtUQzG4GJO-X5dyqQ
https://open.spotify.com/playlist/37i9dQZF1DZ06evO2iBPiw?si=55d0fbfe69a54668
https://open.spotify.com/artist/3WrFJ7ztbogyGnTHbHJFl2?si=xtuxzf2bQUet4KsMI7Ldwg
```
#### Errors
If you encounter any errors, look at `errors.log` to look at the tracks that could not be downloaded.