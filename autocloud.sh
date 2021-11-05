#!/bin/bash
# A shell script that runs the main autocloud script. Keep it in the same
# directory as autocloud/main.py. Add a symbolic link to this script somewhere
# in the PATH.

if [[ -e logs/autocloud_setup.log ]]; then
  :  # already setup
else
  pip install -r requirements.txt
  python autocloud_setup.py
fi

python main.py "$@"  # "$@" passes all parameters this file recieves to main.py
