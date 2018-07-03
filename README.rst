Bunny Bone
==========
.. image:: https://raw.githubusercontent.com/steinwurf/bunny-bone/master/icon.png

This project contains the Arduino (Simblee) code for a data collector which uses
Bluetooth Low Energy (BLE) to communicate readings from a sensor.
Using the python library `gatt <https://github.com/getsenic/gatt-python>`_ the
readings are recieved and written to a file.

The project is very specialized but may be a good example for working with BLE.

Setup bunny bone python application
-----------------------------------

Disclaimer: The bunny bone python application will only run on Linux, and has
only been run on Ubuntu 18.04.

1. Install the dependencies::

    sudo apt-get update
    sudo apt-get install virtualenv python3-pip libdbus-1-dev libglib2.0-dev libgirepository1.0-dev libcairo2-dev git

2. Clone the project::

    git clone https://github.com/steinwurf/bunny-bone


3. Setup the virtual environment::

    cd bunny-bone
    virtualenv -p python3 bluetooth
    source bluetooth/bin/activate
    pip3 install -r requirements.txt

Install the bunny bone desktop launcher
---------------------------------------

Run the following command to install the desktop shortcut and result directory::

    ./install.sh

Now click the new bunny bone icon on the desktop and allow it to execute.

A terminal should show and the results will appear in the
`~/Desktop/bunny-bone-results` folder.

Configuration File
------------------

If you need to configure the python application, you can do so by changing the
`conf.cfg` file.

The configuration file consists of various sections.

DEFAULT section
...............
The DEFAULT section specifies the adapter name to use. This is the adapter name
of the bluetooth device you want to use. You can use this command to get the
name::

    hcitool dev

Example output::

    Devices:
        hci0	00:1C:DE:07:4D:30

Here the name is hci0.

Sensor Sections
...............
Following the DEFAULT section is a set of one or more sensor sections.
The name of each section is the name of the device which we want to read from.
Each sensor section contains an attribute called OutputFile which is the file
which will used to store the results for that sensor.

Please restart the application for the applied changes to take effect.

Simblee
-------
The Arduino code is made for the Simblee board.

Library requirements:

1. CircularBuffer library from Library Manager.
2. HX711 library from github: https://github.com/bogde/HX711

Note: Remember to change the name of the sensor when deploying.
