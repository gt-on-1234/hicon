# cd into the hicon-{username} folder and ensure that hicon-dev is not activated before running
chmod +x tools/update_envionment.sh
conda env remove -n hicon-dev
conda env create
