default: help 
 
.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

FORMAT?=mp3
OUT?=music
.PHONY: run
run:  #  Run download script. Change file format (default mp3) by setting env "make run FORMAT={mp3,flac,ogg,opus,m4a,wav}"
	@echo "Starting download ..."
	@python3 download.py ${FORMAT} ${OUT}
	@echo "Files stored in ${OUT}"

.PHONY: setup
setup: # Setup dependencies
	pip install spotdl
	brew update && brew upgrade
	brew install ffmpeg
	touch urls.txt