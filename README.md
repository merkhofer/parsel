flask_angular
=============

Flask ReST service shows directory and tar file contents with options regex.
This is for class demo purposes only. Don't run this on a publicly accessible server, unless
you want the entire world to see and mess with the contents of your hard drive. 

Two Flask prcoeses need to be run on the command line:
- flask_rest_service.py (change WALK_DIR to some directory on your system to which you have access as yourself).
- flask_angular_service.py (serves the Angular code, does nothing more)

The flask_rest_service provides data for the flask_angular_service. 
