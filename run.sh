#!/bin/bash
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
tmux new-session -d -s App 'cd /home/tdubuntu/Desktop/Project_Prototype_App && export REACT_NATIVE_PACKAGER_HOSTNAME=ubuntuserver.td1932prv.net && npm start'
tmux new-session -d -s Flask 'cd /home/tdubuntu/Desktop/AI_Flask && source venv/bin/activate && uwsgi uwsgi.ini'