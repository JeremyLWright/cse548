sudo apt-get install python-virtualenv python-dev g++
#Create a virtual environment
virtualenv envs/548
# Activate the virtual environment by "sourcing" the activate file
. envs/548/bin/activate
# Install the required tools.
pip install -r requirements.txt


# You are not ready to start the webserver.
python manage.py runserver

# Now connect to 127.0.0.1:8000 with a webbrowser

