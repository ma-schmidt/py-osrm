
Guide for OSRM
==============


Server setup
------------
See: https://github.com/Project-OSRM/osrm-backend/wiki/Building-OSRM
Then: https://github.com/Project-OSRM/osrm-backend/wiki/Running-OSRM

Download maps from: http://download.geofabrik.de/

Tested on Bash on Ubuntu on Windows. Works perfectly.


OSRM_helper Python package
--------------------------

The OSRM_helper package contains the Route class which takes care of:
1. Calling the API through the server
2. Storing the result in a more user-friendly format
3. Allowing the drawing fo the route on an interactive map directly with the method show()
